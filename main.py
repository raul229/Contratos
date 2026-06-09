from dotenv import  load_dotenv
import os
from pathlib import Path
import json
from src.gestorContratos import GestorContratos
from  utilidades.utils import listas_archivos, mostrar_opciones, dividir_texto, completar_fechas
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

def agregar_cuadriculas(pdf, intervalos):
    for pagina in pdf:
        ancho = pagina.rect.width
        alto = pagina.rect.height

        # Líneas verticales cada 50 puntos
        for x in range(0, int(ancho), intervalos):
            pagina.draw_line(
                fitz.Point(x, 0),
                fitz.Point(x, alto),
                color=(0.7, 0.7, 0.7),
                width=0.5
            )

            pagina.insert_text(
                (x + 2, 10),
                str(x),
                fontsize=6
            )

        # Líneas horizontales cada 50 puntos
        for y in range(0, int(alto), intervalos):
            pagina.draw_line(
                fitz.Point(0, y),
                fitz.Point(ancho, y),
                color=(0.7, 0.7, 0.7),
                width=0.5
            )

            pagina.insert_text(
                (2, y + 10),
                str(y),
                fontsize=6
            )

def entel(BASE_DIR, contexto):

    contratos_entel = Path(os.getenv('CONTRATOS_ENTEL'))
    #estraemos todos los documentos en una lista
    documentos= listas_archivos(contratos_entel)

    doc_pruebas=1
    #imprime un archivo en especifico
    print(documentos['otros'][doc_pruebas])
    #escogemos un archivo en especifico ¡
    pdf=fitz.open(documentos['otros'][doc_pruebas])
    
    pagina = pdf[0]
    #agregamos cuadriculas 
    #agregar_cuadriculas(pdf, 10)

    
    ruc = contexto["RUC"]
    razon_social=contexto["RAZON_SOCIAL"]
    rrll=contexto["RRLL"]
    numero_celular=contexto["CELULAR_RRLL"]
    correo=contexto["CORREO_RRLL"]
    dni= contexto["DNI"]
    tamano_fuente=12
    fecha =contexto["FECHA"]
    direccion_instalacion= contexto["DOMICILIO_INSTALACION"]
    nombre_mes=contexto["NOMBRE_MES"]
    dia=contexto["DIA"]
    anio=contexto["ANIO"]
    velocidad=200
    renta_fija="99.90"
    descuento_segun_plan="25.40"
    
    #razon social
    texto, numero_lineas = dividir_texto(razon_social,40) 
    pagina.insert_text(
        (20,260-(tamano_fuente*numero_lineas)),
        texto,
        fontsize=tamano_fuente
    )
    
    #INGRESO DE RUC
    pagina.insert_text(
        (50, 295),
        ruc,
        fontsize=tamano_fuente
    )
    #rrll
    texto, numero_lineas = dividir_texto(rrll,40) 
    pagina.insert_text(
        (20,350-(tamano_fuente*numero_lineas)),
        texto,
        fontsize=tamano_fuente
    )
    
    #TIPO DE DOCUMENTO Y DNI
    pagina.insert_text(
        (25, 400),
        f'DNI {dni}',
        fontsize=tamano_fuente
    )
    #CORREO
    pagina.insert_text(
        (25, 430),
        correo,
        fontsize=tamano_fuente
    )

    #NUMERO DE CONTACTO
    pagina.insert_text(
        (25, 460),
        numero_celular,
        fontsize=tamano_fuente
    )
    #DIRECCION DE INSTALACION
    texto, numero_lineas = dividir_texto(direccion_instalacion,50) 
    pagina.insert_text(
        (20,513-(10*numero_lineas)),
        texto,
        fontsize=10
    )
    pagina.insert_text(
        (20,563-(10*numero_lineas)),
        texto,
        fontsize=10
    )
        
    #VELOCIDAD DE DESCARGA Y SUBIDA
    pagina.insert_text(
        (330, 440),
        f'{velocidad}                {int(velocidad*0.7)}                {velocidad}               {int(velocidad*0.7)}',
        fontsize=tamano_fuente
    )
    
    #CODIGO CLIENTE
    pagina.insert_text(
        (110, 610),
        ruc,
        fontsize=tamano_fuente
    )
    
    #NOMBRE PLAN TARIFARIO
    pagina.insert_text(
        (140, 625),
        f"Pack Empresas {velocidad}",
        fontsize=tamano_fuente
    )
    
    #nombre de la promocion
    pagina.insert_text(
        (140, 640),
        "30% y bono de velocidad por 6m.",
        fontsize=tamano_fuente
    )
    
    #SERVICIO NUEVO
    pagina.insert_text(
        (25, 665),
        'X',
        fontsize=tamano_fuente
    )
    
    #RENTA FIJA
    pagina.insert_text(
        (243, 712),
        renta_fija,
        fontsize=tamano_fuente
    )
    #PAGINA NUMERO 3
    pagina= pdf[2]
    
    #nombre de rrll
    texto, numero_lineas = dividir_texto(rrll,17) 
    pagina.insert_text(
        (195,300-(tamano_fuente*numero_lineas)),
        texto,
        fontsize=tamano_fuente
    )
    
    
    #cargo
    pagina.insert_text(
        (195,330),
        "GERENTE GENERAL",
        fontsize=tamano_fuente
    )
    
    #FECHA
    pagina.insert_text(
        (60, 345),
        fecha,
        fontsize=tamano_fuente
    )
    
    #HORA
    pagina.insert_text(
        (220, 345),
        "10 : 00 : 00",
        fontsize=tamano_fuente
    )
    
    
    #PAGINA NUMERO 5
    pagina= pdf[4]
    
    #nombre de rrll
    texto, numero_lineas = dividir_texto(rrll,17) 
    pagina.insert_text(
        (40,510-(tamano_fuente*numero_lineas)),
        texto,
        fontsize=tamano_fuente
    )
    
    #DNI
    pagina.insert_text(
        (180, 510),
        dni,
        fontsize=tamano_fuente
    )
    
    #cargo
    pagina.insert_text(
        (260,510-tamano_fuente),
        "GERENTE\nGENERAL",
        fontsize=tamano_fuente
    )
    #CELULAR
    texto, numero_lineas = dividir_texto(numero_celular,10) 
    pagina.insert_text(
        (350, 510-(tamano_fuente*numero_lineas)),
        texto,
        fontsize=tamano_fuente
    )
    #correo
    pagina.insert_text(
        (436, 510),
        correo,
        fontsize=9
    )
    
    #dia
    pagina.insert_text(
        (200, 640),
        f"{dia}                                    {nombre_mes}                            {anio}",
        fontsize=tamano_fuente
    )
    
    #nombre de rrll
    pagina.insert_text(
        (100,710),
        rrll,
        fontsize=tamano_fuente
    )
    #cargo
    pagina.insert_text(
        (100,730),
        "GERENTE GENERAL",
        fontsize=tamano_fuente
    )
    
    
    #PAGINA NUMERO 6
    pagina= pdf[5]
    
    #FECHA
    pagina.insert_text(
        (120, 185),
        fecha,
        fontsize=tamano_fuente
    )
    #RUC
    pagina.insert_text(
        (230, 215),
        ruc,
        fontsize=tamano_fuente
    )
    #razon social
    pagina.insert_text(
        (230, 240),
        razon_social,
        fontsize=10
    )
    #representante legal
    pagina.insert_text(
        (230, 260),
        rrll,
        fontsize=10
    )
    #CELULAR 
    pagina.insert_text(
        (230, 280),
        numero_celular,
        fontsize=10
    )
    
     #PAGINA NUMERO 7
    #DIRECCION DE INSTALACION
    texto, numero_lineas = dividir_texto(direccion_instalacion,100) 
    pagina.insert_text(
        (80,340-(10*numero_lineas)),
        texto,
        fontsize=10
    )
    
    pagina= pdf[6]
    
    #FECHA
    pagina.insert_text(
        (120, 185),
        fecha,
        fontsize=tamano_fuente
    )
    #RUC
    pagina.insert_text(
        (230, 225),
        ruc,
        fontsize=tamano_fuente
    )
    #razon social
    pagina.insert_text(
        (230, 250),
        razon_social,
        fontsize=10
    )
    #representante legal
    pagina.insert_text(
        (230, 270),
        rrll,
        fontsize=10
    )
    #CELULAR 
    pagina.insert_text(
        (230, 290),
        numero_celular,
        fontsize=10
    )
    
    #DIRECCION DE INSTALACION
    texto, numero_lineas = dividir_texto(direccion_instalacion,100) 
    pagina.insert_text(
        (80,350-(10*numero_lineas)),
        texto,
        fontsize=10
    )
    
    
    #DESCUENTO  SEGUN PLAN
    pagina.insert_text(
        (230, 430),
        f"S/. {descuento_segun_plan}",
        fontsize=10
    )
    
    #GUARDAR DOCUMENTO
    pdf.save(str(documentos['otros'][doc_pruebas]).replace(".pdf", "-prueba.pdf"))
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
    contexto = completar_fechas(contexto)
    # escoger operador
    operador = mostrar_opciones(['Entel', 'On Empresas'])

    match operador:
        case 'Entel':
            entel(BASE_DIR, contexto)
        case 'On Empresas':
            on_empresas(BASE_DIR, contexto)

if __name__ == '__main__':
    main()










