from dotenv import  load_dotenv
import os
import json
from src.gestorContratos import GestorContratos

def main():

    #cargamos los datos
    with open( 'datos.txt', 'r',encoding='utf-8' ) as d:
        contexto = json.load(d)
        d.close()

    #completamos campos necesarios
    direccion_fiscal = contexto['DOMICILIO_FISCAL']
    fecha = contexto['FECHA'].split('/')
    contexto['DISTRITO'] = direccion_fiscal.split(' - ')[-1]
    contexto['DOMICILIO_FISCAL'] = ' - '.join(direccion_fiscal.split(' - ')[:-1])

    contexto['DIA'] = fecha[0]
    contexto['MES'] = fecha[1]
    contexto['ANIO'] = fecha[2]

    #cargamos variables de entorno
    load_dotenv()

    # nombre de las plantillas de los contratos
    arrendamiento= os.getenv('CONTRATO_ARRENDAMIENTO')
    contactos= os.getenv('CONTACTOS_OFICIALES')
    publicidad = os.getenv('TRATAMIENTO_DATOS')
    anexo = os.getenv('ANEXO')

    carpeta_clientes=os.getenv('RUTA_CLIENTES')
    carpeta_contratos=os.getenv('RUTA_CONTRATOS')
    gestor= GestorContratos( carpeta_clientes, carpeta_contratos)

    #esto te genera las opciones interactivas para contruir la ruta de las platillas
    gestor.construir_ruta_trabajo()

    lista_documentos= [arrendamiento, contactos, publicidad, anexo]
    gestor.llenar_plantilla(lista_documentos, contexto)
    print('convertir a pdf')
    for i in lista_documentos:
        gestor.convertir_a_pdf(i)
        print(i)

    print('CONTRATOS CREADOS!!')

if __name__ == '__main__':
    main()










