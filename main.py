from dotenv import  load_dotenv
import os
from pathlib import Path
import json
from src.gestorContratos import GestorContratos
from  utilidades.utils import listas_archivos

def main():
    
    #ruta base
    BASE_DIR = Path(__file__).resolve().parent
    ruta_datos = BASE_DIR / 'datos.txt'
    ruta_excel_correo = BASE_DIR / 'DATOS CORREO.xlsx'

    #cargamos los datos
    with open( ruta_datos, 'r',encoding='utf-8' ) as d:
        contexto = json.load(d)
        d.close()

    #cargamos variables de entorno
    load_dotenv()

    carpeta_clientes=os.getenv('RUTA_CLIENTES')
    carpeta_contratos=os.getenv('RUTA_CONTRATOS')
    gestor= GestorContratos( carpeta_clientes, carpeta_contratos)

    #esto te genera las opciones interactivas para contruir la ruta de las platillas
    gestor.construir_ruta_trabajo()
        
    #Cargamos el contexto 
    gestor.cargar_contexto(contexto)
    
    #obtenemos todos los archivos de la carpeta obligatorios
    archivos= listas_archivos(gestor.ruta_trabajo)
    lista_documentos= archivos['obligatorios']
    lista_svas= archivos['svas']
    
    gestor.llenar_plantilla(lista_documentos)
    print('convertir a pdf')
    for i in lista_documentos:
        print(i)
        gestor.convertir_a_pdf(i.name)
    
    gestor.llenar_datos_correo(ruta_excel_correo)

    print('CONTRATOS CREADOS!!')

if __name__ == '__main__':
    main()










