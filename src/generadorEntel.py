import fitz
from pathlib import Path

from src.datosEntel import (
    ANEXOS_POR_COMBINACION,
    ARCHIVOS_BASE_POR_PLAN,
    HC_ARCHIVO_POR_PLAN,
    HC_COORDS_POR_PLAN,
    MAPA_ENTEL_POR_ARCHIVO,
    PLANES_ENTEL,
    PROMOCIONES_ENTEL,
    VELOCIDADES_SIN_BONO,
)
from src.generadorContratos import GeneradorContratos
from utilidades.utils import (
    dividir_texto,
    listas_archivos,
    mostrar_opciones,
)


class GeneradorEntel(GeneradorContratos):
    """
    Generador de contratos para Entel.
    A diferencia de On Empresas, los PDF se llenan por coordenadas
    con PyMuPDF en lugar de usar plantillas docxtpl.

    Los planes y mapas de coordenadas viven en `src/datosEntel.py`.
    """

    def __init__(
        self,
        ruta_carpeta_clientes: str | Path,
        ruta_carpeta_contratos: str | Path,
    ) -> None:
        super().__init__(ruta_carpeta_clientes, ruta_carpeta_contratos)

        self.nombre_plan: str | None = None
        self.velocidad: int | None = None
        self.promocion: str | None = None
        self.renta_fija: str | None = None
        self.descuento_segun_plan: str | None = None

    def nombre_operador(self) -> str:
        return 'Entel'

    def usa_excel_correo(self) -> bool:
        return False

    def _es_ruta_valida(self, opciones: list[str]) -> bool:
        # Para Entel la "ruta" es directamente la carpeta de plantillas.
        return True

    # --------------------------------------------------
    # FLUJO ESPECÍFICO
    # --------------------------------------------------

    def ejecutar(self, contexto: dict) -> None:
        self.cargar_contexto(contexto)
        self._pedir_datos_plan()
        self.construir_ruta_trabajo()
        self.preparar_carpetas_cliente()

        self.llenar_plantillas_pdf(self.obtener_plantillas())
        self.llenar_hc()
        self.post_proceso()

    def obtener_plantillas(self) -> list[Path]:
        """
        Devuelve los PDFs del contrato (archivo base + anexos según
        la combinación elegida).
        """
        return self._obtener_plantillas_contrato()

    def obtener_plantillas_hc(self) -> list[Path]:
        """Devuelve el .xlsm de la HC para el plan actual."""
        archivos = listas_archivos(self.ruta_trabajo)
        disponibles = {p.name: p for p in archivos['otros']}
        archivo = HC_ARCHIVO_POR_PLAN[self.nombre_plan]
        if archivo not in disponibles:
            raise FileNotFoundError(
                f'Falta la plantilla HC "{archivo}" en {self.ruta_trabajo}'
            )
        return [disponibles[archivo]]

    def coordenadas_para_xlsx(self, ruta_plantilla: Path) -> dict:
        if ruta_plantilla.name == HC_ARCHIVO_POR_PLAN.get(self.nombre_plan):
            return HC_COORDS_POR_PLAN.get(self.nombre_plan, {})
        return {}

    def _post_procesar_xlsx(self, wb) -> None:
        """
        En la HC ocultamos todas las hojas excepto 'Formulario'
        para que el PDF resultante contenga solo esa página.
        """
        for nombre in wb.sheetnames:
            wb[nombre].sheet_state = (
                'visible' if nombre == 'Formulario' else 'hidden'
            )

    def llenar_hc(self) -> None:
        """Llena la HC del plan y la convierte a PDF en la carpeta del cliente."""
        for plantilla in self.obtener_plantillas_hc():
            self.llenar_una_plantilla(plantilla)
            self._convertir_archivo_a_pdf(plantilla)

    def obtener_plantillas(self) -> list[Path]:
        """
        Devuelve solo los PDFs a llenar para la combinación actual:
        el archivo base del plan + los anexos según promoción.
        """
        archivos = listas_archivos(self.ruta_trabajo)
        disponibles = {p.name: p for p in archivos['otros']}

        archivo_base = ARCHIVOS_BASE_POR_PLAN[self.nombre_plan]
        anexos = ANEXOS_POR_COMBINACION.get(
            (self.nombre_plan, self.velocidad, self.promocion),
            [],
        )

        nombres = [archivo_base] + anexos
        rutas: list[Path] = []
        for nombre in nombres:
            if nombre not in disponibles:
                raise FileNotFoundError(
                    f'Falta la plantilla "{nombre}" en {self.ruta_trabajo}'
                )
            rutas.append(disponibles[nombre])
        return rutas

    def post_proceso(self) -> None:
        print('CONTRATOS ENTEL CREADOS!!')

    def _pedir_datos_plan(self) -> None:
        print('Seleccione el producto:')
        self.nombre_plan = mostrar_opciones(['Internet Empresas', 'Pack Empresas'])

        print('Seleccione la velocidad de internet (Mbps):')
        self.velocidad = int(mostrar_opciones(['200', '300', '500', '1000']))

        # Las promociones permitidas dependen de la velocidad
        # (p.ej. 1000 Mbps no admite bono de velocidad).
        opciones_promo = self._promociones_permitidas()
        print('Promociones a aplicar:')
        self.promocion = mostrar_opciones(opciones_promo)

        plan = PLANES_ENTEL[self.nombre_plan][self.velocidad]
        self.renta_fija = str(plan['renta'])
        self.descuento_segun_plan = str(plan['descuento'])

    def _promociones_permitidas(self) -> list[str]:
        if self.velocidad in VELOCIDADES_SIN_BONO:
            # 1000 Mbps: solo descuento (sin bono de velocidad).
            return [p for p in PROMOCIONES_ENTEL if 'bono' not in p]
        return list(PROMOCIONES_ENTEL)

    # --------------------------------------------------
    # LLENADO PDF (multi-archivo)
    # --------------------------------------------------

    def llenar_plantillas_pdf(self, plantillas: list[Path]) -> None:
        for ruta in plantillas:
            self._llenar_un_pdf(ruta)

    def _llenar_un_pdf(self, ruta_plantilla: Path) -> None:
        pdf = fitz.open(ruta_plantilla)
        try:
            paginas = MAPA_ENTEL_POR_ARCHIVO.get(ruta_plantilla.name, {})
            for num_pagina, coords in paginas.items():
                if num_pagina >= len(pdf):
                    raise IndexError(
                        f'El PDF {ruta_plantilla.name} no tiene la '
                        f'página {num_pagina} (tiene {len(pdf)}).'
                    )
                self._poblar_pagina(pdf[num_pagina], coords)

            salida = self.editables_cliente / ruta_plantilla.name
            pdf.save(str(salida))
        finally:
            pdf.close()

        destino = self.carpeta_cliente / ruta_plantilla.name
        salida.replace(destino)

    # --------------------------------------------------
    # MOTOR GENÉRICO DE LLENADO POR COORDENADAS
    # --------------------------------------------------

    def _datos_generador(self) -> dict:
        """Datos calculados por el propio generador (plan, renta, etc.)."""
        plan = PLANES_ENTEL.get(self.nombre_plan or '', {}).get(
            self.velocidad or 0, {}
        )
        return {
            '_PROMOCION': self.promocion,
            '_RENTA_FIJA': self.renta_fija,
            '_DESCUENTO': self.descuento_segun_plan,
            '_NOMBRE_PLAN': self.nombre_plan,
            '_VELOCIDAD': self.velocidad,
            **plan,
        }

    def _resolver_valor(self, campo: str, opciones: dict) -> str | None:
        """
        Resuelve el valor a insertar para un campo.
        Prioridad:
            1. 'value' literal
            2. 'transform' aplicado al contexto
            3. campo del contexto del cliente
            4. campo de los datos del generador
        """
        if 'value' in opciones:
            return opciones['value']

        if 'transform' in opciones:
            return self._aplicar_transform(opciones['transform'])

        nombre_real = opciones.get('field', campo)
        if nombre_real in (self.contexto or {}):
            return self.contexto[nombre_real]
        if nombre_real in self._datos_generador():
            return self._datos_generador()[nombre_real]
        return None

    def _aplicar_transform(self, nombre: str) -> str | None:
        ctx = self.contexto or {}
        if nombre == 'doc_y_dni':
            return f"{ctx.get('TIPO_DOCUMENTO_RRLL', '')} {ctx.get('DNI', '')}".strip()
        if nombre == 'velocidades':
            v = self.velocidad or 0
            return f"{v}                {int(v * 0.7)}               {v}             {int(v * 0.7)}"
        if nombre == 'nombre_plan':
            return f"{self.nombre_plan} {self.velocidad}"
        if nombre == 'dia_mes_anio':
            return (
                f"{ctx.get('DIA', '')}                                    "
                f"{ctx.get('NOMBRE_MES', '')}                            "
                f"{ctx.get('ANIO', '')}"
            )
        if nombre == 'descuento':
            return f"S/. {self.descuento_segun_plan}"
        return None

    def _poblar_pagina(self, pagina, coords: dict) -> None:
        for campo, (x, y, opciones) in coords.items():
            valor = self._resolver_valor(campo, opciones)
            if valor is None:
                continue

            tamano = opciones.get('tamano', 12)
            max_caracteres = opciones.get('max_caracteres')
            if max_caracteres:
                texto, lineas = dividir_texto(str(valor), max_caracteres)
                y_inicial = y - (tamano * lineas)
            else:
                texto = str(valor)
                y_inicial = y

            pagina.insert_text(
                (x, y_inicial),
                texto,
                fontsize=tamano,
            )
