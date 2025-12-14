from pathlib import Path
import platform
from docxtpl import DocxTemplate
from xlsxtpl.writerx import BookWriter
from subprocess import run
from utilidades.utils import generar_opciones, mostrar_opciones


class GestorContratos:
    def __init__(self, ruta_carpeta_clientes: str | Path, ruta_carpeta_contratos: str | Path) -> None:
        self.ruta_carpeta_clientes = Path(ruta_carpeta_clientes)
        self.ruta_carpeta_contratos = Path(ruta_carpeta_contratos)

        self.contexto: dict | None = None

        self.carpeta_cliente: Path | None = None
        self.editables_cliente: Path | None = None

        self.sistema_operativo: str | None = None
        self.convert = None

        # Ruta de trabajo SIEMPRE como Path
        self.ruta_trabajo: Path | None = None

        self.verificar_os()

    # --------------------------------------------------
    # CONSTRUCCIÓN DE RUTA
    # --------------------------------------------------

    def construir_ruta_trabajo(self) -> None:
        ruta_actual = self.ruta_carpeta_contratos

        while True:
            opciones = generar_opciones(ruta_actual)

            if '0. Obligatorios' in opciones:
                break

            opcion = mostrar_opciones(opciones)
            ruta_actual = ruta_actual / opcion

        self.ruta_trabajo = ruta_actual

    # --------------------------------------------------
    # SISTEMA OPERATIVO
    # --------------------------------------------------

    def verificar_os(self) -> None:
        if platform.system() == 'Windows':
            from docx2pdf import convert
            self.convert = convert
            self.sistema_operativo = 'Windows'
        else:
            self.sistema_operativo = 'Linux'

    # --------------------------------------------------
    # CARPETAS CLIENTE
    # --------------------------------------------------

    def crear_carpeta_cliente(self) -> None:
        self.carpeta_cliente = self.ruta_carpeta_clientes / f'{self.contexto["RAZON_SOCIAL"]}-{self.contexto["RUC"]}'
        self.editables_cliente = self.carpeta_cliente / 'EDITABLES'

        self.carpeta_cliente.mkdir(exist_ok=True)
        self.editables_cliente.mkdir(exist_ok=True)
        (self.carpeta_cliente / 'DOC ADICIONALES').mkdir(exist_ok=True)

    # --------------------------------------------------
    # LLENADO DE PLANTILLAS
    # --------------------------------------------------

    def _llenar_docx(self, ruta_plantilla: Path) -> None:
        docx = DocxTemplate(ruta_plantilla)
        docx.render(self.contexto)
        docx.save(self.editables_cliente / ruta_plantilla.name)

    def _llenar_xlsx(self, ruta_plantilla: Path) -> None:
        xlsx = BookWriter(ruta_plantilla)
        xlsx.render_book(self.contexto)
        xlsx.save(self.editables_cliente / ruta_plantilla.name)

    def llenar_plantilla(self, nombre_plantilla: str | list[str], contexto: dict) -> None:
        self.contexto = contexto
        self.crear_carpeta_cliente()

        if isinstance(nombre_plantilla, list):
            rutas = [
                self.ruta_trabajo / '0. Obligatorios' / nombre
                for nombre in nombre_plantilla
            ]
        else:
            rutas = [self.ruta_trabajo / '0. Obligatorios' / nombre_plantilla]

        for ruta in rutas:
            if ruta.suffix == '.docx':
                self._llenar_docx(ruta)
            elif ruta.suffix in ('.xlsx', '.xlsm'):
                self._llenar_xlsx(ruta)
            else:
                raise ValueError(f'Formato no soportado: {ruta.name}')

    # --------------------------------------------------
    # CONVERSIÓN A PDF
    # --------------------------------------------------

    def convertir_a_pdf(self, nombre_archivo: str) -> None:
        ruta_origen = self.editables_cliente / nombre_archivo

        if self.sistema_operativo == 'Linux':
            run([
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', str(self.carpeta_cliente),
                str(ruta_origen)
            ], check=True)

        else:
            if ruta_origen.suffix != '.docx':
                raise ValueError('En Windows solo se convierten archivos .docx')

            ruta_pdf = self.carpeta_cliente / ruta_origen.with_suffix('.pdf').name
            self.convert(str(ruta_origen), str(ruta_pdf))
