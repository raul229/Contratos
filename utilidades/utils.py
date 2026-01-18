from pathlib import Path

def generar_opciones( ruta: Path) -> list[str]:
    if not ruta.is_dir():
        return []
    return [p.name for p in ruta.iterdir() if p.is_dir()]

def mostrar_opciones( lista_opciones: list[str]) -> str:
    print('Puedes escoger entre las siguientes opciones:')
    for index, opcion in enumerate(lista_opciones):
        print(index, '-', opcion)

    try:
        respuesta = int(input('Respuesta: '))
        return lista_opciones[respuesta]
    except (ValueError, IndexError):
        print('Opción inválida')
        return mostrar_opciones(lista_opciones)

def listas_archivos(ruta: Path):
    lista = []
    ruta = ruta / '0. Obligatorios'
    for archivo in ruta.iterdir():
        lista.append(archivo)
    return lista
