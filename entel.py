import os
from pathlib import Path
import fitz
from  utilidades.utils import  dividir_texto, listas_archivos, mostrar_opciones

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

    ruc = contexto["RUC"]
    razon_social=contexto["RAZON_SOCIAL"]
    rrll=contexto["RRLL"]
    numero_celular=contexto["CELULAR_RRLL"]
    correo=contexto["CORREO_RRLL"]
    dni= contexto["DNI"]
    tipo_documento_rrll=contexto["TIPO_DOCUMENTO_RRLL"]
    tamano_fuente=12
    fecha =contexto["FECHA"]
    direccion_instalacion= contexto["DOMICILIO_INSTALACION"]
    nombre_mes=contexto["NOMBRE_MES"]
    dia=contexto["DIA"]
    anio=contexto["ANIO"]
    #DATOS FALTANTES 
    print("Seleccione el producto:")
    nombre_plan= mostrar_opciones(["Internet Empresas", "Pack Empresas"])
    print("Seleccione la velocidad de intertet (Mbps):")
    respuesta= mostrar_opciones(["200", "300", "500", "1000"])
    velocidad=int(respuesta)
    print("Promociones a plicar:")
    promocion=mostrar_opciones(["bono de velocidad por 6m", "Solo 30% por 6m.", "30% y bono de velocidad por 6m"])
    planes = {
    "Internet Empresas": {
        200: {"renta": 90.00, "descuento": 22.88},
        300: {"renta": 120.00, "descuento": 30.51},
        500: {"renta": 150.00, "descuento": 38.14},
        1000: {"renta": 180.00, "descuento": 45.76},
    },
    "Pack Empresas": {
        200: {"renta": 99.90, "descuento": 25.40},
        300: {"renta": 129.90, "descuento": 33.03},
        500: {"renta": 159.90, "descuento": 40.65},
        1000: {"renta": 189.90, "descuento": 48.28},
    }
}

    
    
    renta_fija=str(planes[nombre_plan][velocidad]["renta"])
    descuento_segun_plan =str(planes[nombre_plan][velocidad]["descuento"])


    contratos_entel = Path(os.getenv('CONTRATOS_ENTEL'))
    #estraemos todos los documentos en una lista
    documentos= listas_archivos(contratos_entel)

    doc_pruebas=1
    #imprime un archivo en especifico
    print(documentos['otros'][doc_pruebas])
    #escogemos un archivo en especifico ¡
    pdf=fitz.open(documentos['otros'][doc_pruebas])
    
    pagina_actual = pdf[0]
    #agregamos cuadriculas 
    #agregar_cuadriculas(pdf, 10)


    def insertar_texto(x:int, y:int, texto, tamano_fuente:float=12):
        pagina_actual.insert_text(
            (x, y),
            str(texto),
            fontsize=tamano_fuente
        )

    def insertar_texto_extenso(x:int, y:int, texto, max_caracteres:int=40,tamano_fuente:float=12, ):
        texto_varias_lineas, lineas = dividir_texto(texto,max_caracteres)
        insertar_texto(x,y-(tamano_fuente*lineas),texto_varias_lineas , tamano_fuente)

    #razon social
    insertar_texto_extenso(20,260, razon_social, tamano_fuente=9)
    
    #INGRESO DE RUC
    insertar_texto(50, 295, ruc)

    #rrll
    insertar_texto_extenso(20,350, rrll)
       
    #TIPO DE DOCUMENTO Y DNI
    insertar_texto(25, 400, f"{tipo_documento_rrll} {dni}" )

    #CORREO
    insertar_texto(25, 430, correo)
    
    #NUMERO DE CONTACTO
    insertar_texto(25, 460, numero_celular)
    
    #DIRECCION DE INSTALACION
    insertar_texto_extenso(20,513, direccion_instalacion, max_caracteres=60, tamano_fuente=8)

    insertar_texto_extenso(20,563, direccion_instalacion, max_caracteres=60, tamano_fuente=8)
            
    #VELOCIDAD DE DESCARGA Y SUBIDA
    insertar_texto(330, 440,f"{velocidad}                {int(velocidad*0.7)}               {velocidad}             {int(velocidad*0.7)}" )
        
    #CODIGO CLIENTE
    insertar_texto(110, 610, ruc)
       
    #NOMBRE PLAN TARIFARIO
    insertar_texto(140,625, f"{nombre_plan} {velocidad}")
        
    #nombre de la promocion
    insertar_texto(140, 640, promocion)
       
    #SERVICIO NUEVO
    insertar_texto(25, 665, "X")
       
    #RENTA FIJA
    insertar_texto(243, 712, renta_fija)
   
    #PAGINA NUMERO 3
    pagina_actual= pdf[2]
    
    #nombre de rrll
    insertar_texto_extenso(195,300,rrll,max_caracteres=17)
       
    #cargo
    insertar_texto(195,330,"GERENTE GENERAL")
       
    #FECHA
    insertar_texto(60, 345, fecha)
       
    #HORA
    insertar_texto(220, 345,"10 : 00 : 00" )  
    
    #PAGINA NUMERO 5
    pagina_actual= pdf[4]
    
    #nombre de rrll
    insertar_texto_extenso(40,510,rrll, max_caracteres=17 )
        
    #DNI
    insertar_texto(180, 510, dni)
       
    #cargo
    insertar_texto(260,510-tamano_fuente,"GERENTE\nGENERAL" )
    
    #CELULAR
    insertar_texto_extenso(350, 510, numero_celular, max_caracteres=10)
   
    #correo
    insertar_texto_extenso(436,510,correo,tamano_fuente=9,max_caracteres=27 )
    #insertar_texto(436, 510, correo, 9)
       
    # dia / mes / año
    insertar_texto(200, 640,f"{dia}                                    {nombre_mes}                            {anio}" )
        
    #nombre de rrll
    insertar_texto(90,710, rrll, tamano_fuente=10)

    #cargo
    insertar_texto(100,730, "GERENTE GENERAL") 
    
    #PAGINA NUMERO 6
    pagina_actual= pdf[5]
    
    #FECHA
    insertar_texto(120, 185, fecha )
    
    #RUC
    insertar_texto(230, 215, ruc)

    #razon social
    insertar_texto_extenso(225, 240, razon_social, max_caracteres=50, tamano_fuente=10)
    
    #representante legal
    insertar_texto(230, 260, rrll, 10)
    
    #CELULAR 
    insertar_texto(230, 280,numero_celular, 10 )
        
    #DIRECCION DE INSTALACION
    insertar_texto_extenso(80,340, direccion_instalacion, max_caracteres=70, tamano_fuente=12)
   
    #PAGINA NUMERO 7
    
    pagina_actual= pdf[6]
    
    #FECHA
    insertar_texto(120, 185, fecha)
   
    #RUC
    insertar_texto(230, 225, ruc)
    
    #razon social
    insertar_texto_extenso(225, 248, razon_social, max_caracteres=50, tamano_fuente=10)    
    #representante legal
    insertar_texto(230, 270,rrll, 10 )
   
    #CELULAR
    insertar_texto(230, 290, numero_celular, 10)
        
    #DIRECCION DE INSTALACION
    insertar_texto_extenso(80,350, direccion_instalacion, max_caracteres=70, tamano_fuente=12)
   
    #DESCUENTO  SEGUN PLAN
    insertar_texto(230, 430, ("S/. " + descuento_segun_plan) )
        
    #GUARDAR DOCUMENTO
    pdf.save(str(documentos['otros'][doc_pruebas]).replace(".pdf", "-prueba.pdf"))
    pdf.close()

