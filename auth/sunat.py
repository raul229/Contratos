from playwright.sync_api import sync_playwright
import time

def obtener_datos_sunat():


    link = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chromium")
        pagina = browser.new_page()

        pagina.goto(link)

        pagina.fill("#txtRuc", "20123456789")
        
        pagina.click("#btnAceptar")
        print("Inicia sesión manualmente es necesario...")

        input("presiona entel para terminar")
        browser.close()

        return None
    
    
obtener_datos_sunat()