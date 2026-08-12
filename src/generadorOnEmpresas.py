from pathlib import Path

from src.generadorContratos import GeneradorContratos
from utilidades.utils import listas_archivos


class GeneradorOnEmpresas(GeneradorContratos):
    """Generador de contratos para On Empresas / On Negocios."""

    def __init__(
        self,
        ruta_carpeta_clientes: str | Path,
        ruta_carpeta_contratos: str | Path,
        ruta_excel_correo: str | Path,
    ) -> None:
        super().__init__(ruta_carpeta_clientes, ruta_carpeta_contratos)
        self._ruta_excel_correo = Path(ruta_excel_correo)

    def nombre_operador(self) -> str:
        return 'On Empresas'

    def ruta_excel_correo(self) -> Path:
        return self._ruta_excel_correo

    def obtener_plantillas(self) -> list[Path]:
        archivos = listas_archivos(self.ruta_trabajo)
        return list(archivos['obligatorios'])

    def post_proceso(self) -> None:
        print('CONTRATOS ON EMPRESAS CREADOS!!')

    # --------------------------------------------------
    # COMPLETADO DE CONTEXTO (específico de On Empresas)
    # --------------------------------------------------

    def _completar_datos_particulares(self, contexto: dict) -> None:
        lista_respuestas = ['si', 's']

        respuesta = input('\n¿El contrato será con firma digital? (s/n):\n> ')
        es_digital = respuesta.lower() in lista_respuestas

        respuesta = input('\n¿La venta es un producto empresas? (s/n):\n> ')
        es_empresas = respuesta.lower() in lista_respuestas

        contexto.update({
            'ES_DIGITAL': es_digital,
            'ES_EMPRESAS': es_empresas,
        })

        direccion = contexto.get('DOMICILIO_FISCAL', '')
        if ' - ' in direccion:
            partes = direccion.split(' - ')
            contexto['DISTRITO'] = partes[-1]
            contexto['DOMICILIO_FISCAL'] = ' - '.join(partes[:-1])

        self._autocompletar_contactos(contexto)

    def _autocompletar_contactos(self, contexto: dict) -> None:
        nombre = contexto.get('RRLL', '')
        dni = contexto.get('DNI', '')
        correo = contexto.get('CORREO_RRLL', '')
        celular = contexto.get('CELULAR_RRLL', '')

        if not (
            contexto.get('NOMBRE_ADMINISTRATIVO')
            and contexto.get('DNI_ADMINISTRATIVO')
            and contexto.get('CORREO_ADMINISTRATIVO')
            and contexto.get('CELULAR_ADMINISTRATIVO')
        ):
            contexto['NOMBRE_ADMINISTRATIVO'] = nombre
            contexto['DNI_ADMINISTRATIVO'] = dni
            contexto['CORREO_ADMINISTRATIVO'] = correo
            contexto['CELULAR_ADMINISTRATIVO'] = celular

        if not (
            contexto.get('NOMBRE_OPERATIVO')
            and contexto.get('DNI_OPERATIVO')
            and contexto.get('CORREO_OPERATIVO')
            and contexto.get('CELULAR_OPERATIVO')
        ):
            contexto['NOMBRE_OPERATIVO'] = nombre
            contexto['DNI_OPERATIVO'] = dni
            contexto['CORREO_OPERATIVO'] = correo
            contexto['CELULAR_OPERATIVO'] = celular
