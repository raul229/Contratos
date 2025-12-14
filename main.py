from dotenv import  load_dotenv
import os
from src.gestorContratos import GestorContratos

direccion_fiscal = 'CAL.LUIGGI BARSATO NRO. 167 LIMA - LIMA - SAN BORJA'
fecha = '01/01/2024'

lista_fecha = fecha.split('/')

contexto = {
    'RAZON_SOCIAL': 'SYNERFYSOFT SAC',
    'RUC': '20606012345',
    'DOMICILIO_FISCAL': ' '.join(direccion_fiscal.split(' - ')[:-1]),
    'DISTRITO': direccion_fiscal.split(' - ')[-1],
    'RRLL': 'JUAN PEREZ GONZALES',
    'DNI': '12345678',
    'PARTIDA_REGISTRAL': '12345678',
    'FECHA': fecha,
    'DIA': lista_fecha[0],
    'MES': lista_fecha[1],
    'ANIO': lista_fecha[2],
    'CORREO_RRLL': 'correo@rrll.com',
    'CELULAR_RRLL': '985478589',
    'NOMBRE_ADMINISTRATIVO': 'nombre admin prueba',
    'DNI_ADMINISTRATIVO': '85478547',
    'CORREO_ADMINISTRATIVO': 'correo@admin.com',
    'CELULAR_ADMINISTRATIVO': '985478589',
    'NOMBRE_OPERATIVO': 'nombre operativo prueba',
    'DNI_OPERATIVO': '85478547',
    'CORREO_OPERATIVO': 'correo@opetativo.com',
    'CELULAR_OPERATIVO': '985478589',

}

# esta es al ruta a la plantilla con los campos para remplazar
nombre_plantilla= 'Contrato de Arrendamiento de Circuitos ON Negocios v2.0.docx'
#nombre_plantilla= 'Anexo Contactos Oficiales_.docx'
#nombre_plantilla = 'Anexo-Autorización tratamiento datos personales.docx'
#excel = 'ANEXO - Internet ON Negocios 159 v1.0.xlsx'


load_dotenv()
carpeta_clientes=os.getenv('RUTA_CLIENTES')
carpeta_contratos=os.getenv('RUTA_CONTRATOS')
gestor= GestorContratos( carpeta_clientes, carpeta_contratos)
#esto te genera las opciones interactivas para contruir la ruta de las platillas
gestor.construir_ruta_trabajo()
print('putno main')

gestor.llenar_plantilla([nombre_plantilla, 'Anexo Contactos Oficiales_.docx'], contexto)
print('convertir a pdf')
gestor.convertir_a_pdf(nombre_plantilla)
gestor.convertir_a_pdf('Anexo Contactos Oficiales_.docx')









