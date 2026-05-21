from dotenv import  load_dotenv
import os
from pathlib import Path
import json
from src.gestorContratos import GestorContratos
from  utilidades.utils import listas_archivos, mostrar_opciones
import fitz

def on_empresas(BASE_DIR, contexto):

    ruta_excel_correo = BASE_DIR / 'DATOS CORREO.xlsx'

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

def entel(BASE_DIR, contexto):

    contratos_entel = Path(os.getenv('CONTRATOS_ENTEL'))
    #estraemos todos los documentos en una lista
    documentos= listas_archivos(contratos_entel)

    doc_pruebas=6
    #imprime un archivo en especifico
    print(documentos['otros'][doc_pruebas])
    #escogemos un archivo en especifico ¡
    pdf=fitz.open(documentos['otros'][doc_pruebas])
    for pagina in pdf:
        widgets = pagina.widgets()

        if widgets:
            for campo in widgets:
                nombre=campo.field_name
                print(nombre)
                print(contexto[nombre])
                if nombre in contexto:
                    #campo.field_value=contexto[nombre]
                    #campo.update()


                    # obtener posicion
                    rect = campo.rect

                    # escribir texto fijo
                    pagina.insert_text(
                        (rect.x0 + 2, rect.y1 - 5),
                        contexto[nombre],
                        fontsize=10
                    )

                    # eliminar widget
                    pagina.delete_widget(campo)


    pdf.save(f'{str(documentos['otros'][doc_pruebas]).replace(".pdf", "")}-prueba.pdf')
    pdf.close()



def main():
    # cargamos variables de entorno
    load_dotenv()

    # ruta base
    BASE_DIR = Path(__file__).resolve().parent

    ruta_datos = BASE_DIR / 'datos.txt'

    # cargamos los datos
    with open(ruta_datos, 'r', encoding='utf-8') as d:
        contexto = json.load(d)
        d.close()

    # escoger operador
    operador = mostrar_opciones(['Entel', 'On Empresas'])

    match operador:
        case 'Entel':
            entel(BASE_DIR, contexto)
        case 'On Empresas':
            on_empresas(BASE_DIR, contexto)

if __name__ == '__main__':
    main()










