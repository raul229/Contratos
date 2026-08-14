"""Regenera el PDF de prueba de Pack Empresas después de cada guardado.

Ejecutar desde WSL:
    .venv/bin/python test/vigilar_pack_empresas.py
"""

from __future__ import annotations

from pathlib import Path
from subprocess import run
import sys
import time


RAIZ = Path(__file__).resolve().parent.parent
PRUEBA = RAIZ / 'test' / 'test_pack_empresas_pdf.py'
ARCHIVOS_VIGILADOS = (
    PRUEBA,
    RAIZ / 'src' / 'datosEntel.py',
    RAIZ / 'src' / 'generadorEntel.py',
    RAIZ / 'CONTRATOS_ENTEL' / 'pack empresas.pdf',
)
INTERVALO_SEGUNDOS = 0.5


def marcas_de_tiempo() -> dict[Path, int | None]:
    """Devuelve la marca de modificación de cada archivo vigilado."""
    return {
        archivo: archivo.stat().st_mtime_ns if archivo.exists() else None
        for archivo in ARCHIVOS_VIGILADOS
    }


def ejecutar_prueba() -> None:
    print('\nGenerando PDF de prueba de Pack Empresas...')
    resultado = run([sys.executable, '-m', 'pytest', str(PRUEBA), '-q'])
    salida = RAIZ / 'test' / 'salidas' / 'CLIENTE-20123456789' / 'pack empresas - prueba.pdf'
    if resultado.returncode == 0:
        print(f'PDF actualizado: {salida}')
    else:
        print('La prueba falló. Corrige el error y guarda un archivo para reintentar.')


def main() -> None:
    print('Vigilando cambios para Pack Empresas. Presiona Ctrl+C para detener.')
    ejecutar_prueba()
    anterior = marcas_de_tiempo()

    try:
        while True:
            time.sleep(INTERVALO_SEGUNDOS)
            actual = marcas_de_tiempo()
            if actual != anterior:
                # Se actualiza antes de ejecutar para no reaccionar a un único guardado dos veces.
                anterior = actual
                ejecutar_prueba()  # run() espera el fin de pytest antes de continuar.
                anterior = marcas_de_tiempo()
    except KeyboardInterrupt:
        print('\nVigilancia detenida.')


if __name__ == '__main__':
    main()
