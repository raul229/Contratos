from dotenv import  load_dotenv
import os
import json
from src.gestorContratos import GestorContratos
from  utilidades.utils import listas_archivos

def main():

    #cargamos los datos
    with open( 'datos.txt', 'r',encoding='utf-8' ) as d:
        contexto = json.load(d)
        d.close()

    #cargamos variables de entorno
    load_dotenv()

    carpeta_clientes=os.getenv('RUTA_CLIENTES')
    carpeta_contratos=os.getenv('RUTA_CONTRATOS')
    gestor= GestorContratos( carpeta_clientes, carpeta_contratos)

    #esto te genera las opciones interactivas para contruir la ruta de las platillas
    gestor.construir_ruta_trabajo()

    #obtenemos todos los archivos de la carpeta obligatorios
    lista_documentos= listas_archivos(gestor.ruta_trabajo)

    gestor.llenar_plantilla(lista_documentos, contexto)
    print('convertir a pdf')
    for i in lista_documentos:
        print(i)
        gestor.convertir_a_pdf(i.name)

    print('CONTRATOS CREADOS!!')

if __name__ == '__main__':
    main()










