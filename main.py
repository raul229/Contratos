import json
from pathlib import Path

from dotenv import load_dotenv

from src.fabrica import construir_generador, elegir_operador
from utilidades.utils import completar_fechas


def main() -> None:
    load_dotenv()

    base_dir = Path(__file__).resolve().parent
    ruta_datos = base_dir / 'datos.txt'

    with open(ruta_datos, 'r', encoding='utf-8') as f:
        contexto = json.load(f)

    contexto = completar_fechas(contexto)

    operador = elegir_operador()
    generador = construir_generador(operador, base_dir)
    generador.ejecutar(contexto)


if __name__ == '__main__':
    main()
