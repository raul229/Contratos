from dotenv import  load_dotenv
from pathlib import Path
import json
from  utilidades.utils import mostrar_opciones, completar_fechas
from on_empresas import on_empresas
from entel import entel

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










