from pathlib import Path
import  platform
from docxtpl import DocxTemplate
from xlsxtpl.writerx import BookWriter



class GestorContratos:
    def __init__(self, ruta_carpeta_clientes:str|Path, ruta_carpeta_contratos:str|Path)->None:
        self.ruta_carpeta_clientes = Path(ruta_carpeta_clientes)
        self.ruta_carpeta_contratos = Path(ruta_carpeta_contratos )
        self.contexto=None
        # ruta contruida a partir de ruta trabajo
        self.editables_cliente=None
        self.carpeta_cliente=None
        self.sistema_operativo= None
        #verificamos el sistema operativo
        self.verificar_os()
        # almacena los string para convertir la ruta del plan
        # para trabajar con esta se debe agregar la carpeta oblidatorios o svas
        self.ruta_trabajo= []
        self.documentos_obligatorios = []

    def generar_opciones(self, ruta: str | Path) -> list:
        ruta = Path(ruta)
        if not ruta.is_dir():
            return []
        return [p.name for p in ruta.iterdir()]

    def mostrat_opciones(self,lita_opciones: list[str])->str:
        print('Puedes escoger entre los siguientes planes: ')
        for index, opcion in enumerate(lita_opciones):
            print(index, '-', opcion)
        respuesta = int(input('Respuesta: '))
        return lita_opciones[respuesta]


    def construir_ruta_trabajao(self)->None:
        self.ruta_trabajo.append(self.ruta_carpeta_contratos)
        while True:
            #optener las opciones de la carpeta contratos
            lista_opciones = self.generar_opciones((str(Path(*self.ruta_trabajo))))
            #si esta la carpeta de obligatorios en la lista rompe el bucle
            if '0. Obligatorios' in lista_opciones:
                break
            opcion_seleccionada= self.mostrat_opciones(lista_opciones)
            self.ruta_trabajo.append(opcion_seleccionada)

        return

    def verificar_os(self)->None:

        if platform.system() == 'Windows':
            from docx2pdf import convert
            self.convert = convert
            self.sistema_operativo='Windows'
            return
        else:
            from subprocess import run
            self.run = run
            self.sistema_operativo='Linux'

    def converti_a_pdf(self, nombre_archivo:str|Path):


        if self.sistema_operativo == 'Linux':
            self.run([
                'libreoffice',
                '--headless',
                '--convert-to',
                'pdf',
                '--outdir', str(self.carpeta_cliente),  # libreoffice no acepta Path directamente
                str(Path(self.editables_cliente, nombre_archivo))
            ])

        else:
            if '.docx' in nombre_archivo:
                ruta_archivo=str(Path(self.editables_cliente, nombre_archivo))
                ruta_guardar_pdf=str(Path(self.carpeta_cliente, nombre_archivo.replace('.docx', '.pdf')))

                self.convert(ruta_archivo, ruta_guardar_pdf)
            else:
                pass


    def crea_carpeta_cliente(self):
        #guardamos la ruta a la carpeta del cliente
        self.carpeta_cliente = Path(self.ruta_carpeta_clientes / f'{self.contexto["RAZON_SOCIAL"]}-{self.contexto["RUC"]}')

        carpeta_cliente = self.carpeta_cliente
        self.editables_cliente = carpeta_cliente / 'EDITABLES'
        if carpeta_cliente.exists():
            return
        carpeta_cliente.mkdir()
        self.editables_cliente.mkdir()
        (carpeta_cliente / 'DOC ADICONALES').mkdir()


    def _llenar_docx(self, nombre):
        docx = DocxTemplate(nombre)
        docx.render(self.contexto)
        docx.save(str(Path(self.editables_cliente, nombre)))

    def _llenar_xlsx(self, nombre):
        xlsx = BookWriter(nombre)
        xlsx.render_book(self.contexto)
        xlsx.save(str(Path(self.editables_cliente, nombre)))


    def llenar_plantilla(self, nombre_plantilla:str|Path|list[str], contexto:dict)->None:
        #guardamos el conteto para evitar erroroes al crear la carpeta del cliente
        self.contexto = contexto
        ##creamos la carpeta del cliente
        self.crea_carpeta_cliente()
        ## si el parametro es una lista
        #genera uns lista con las rutas completas por cada objeto de las lista
        if isinstance(nombre_plantilla, list):
            lista_nombres_plantillas= [str(Path(*self.ruta_trabajo, '0. Obligatorios', nombre) for nombre in nombre_plantilla)]
            ##se paramos por tipo de archivo
            docxs=[ a for a in lista_nombres_plantillas if a.endswith('.docx')]
            #verificamos que tengamos al menos un elemento
            if len(docxs)>0:
                #recorremos la lista de docxs
                for nombre in docxs:
                    self._llenar_docx(nombre)
            xlsxs= [ a for a in lista_nombres_plantillas if a.endswith('.xlsx') or a.endswith('.xlsm')]

            if len(xlsxs) >0:
                for nombre in xlsxs:
                    self._llenar_xlsx(nombre)
        else:

            ##creamos la ruta de trabajaco completa, con la carpeta obligatorio y el nombre del archivo
            plantilla = str(Path(*self.ruta_trabajo, '0. Obligatorios', nombre_plantilla))
            if plantilla.endswith('.docx'):
                self._llenar_docx(plantilla)
            elif plantilla.endswith('.xlsx') or plantilla.endswith('.xlsm'):
                self._llenar_xlsx(plantilla)
            else:
                print('archivo con con extension no compatible, debe ser .docx, .xlsx, .xlsm')








