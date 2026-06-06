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
    resultado = {
        'obligatorios': [],
        'svas': [],
        'otros': []
    }

    ruta_obligatorios = ruta / '0. Obligatorios'
    ruta_svas = ruta / '1. SVAs'

    # Obligatorios (si existe)
    if ruta_obligatorios.exists():
        resultado['obligatorios'] = [
            a for a in ruta_obligatorios.iterdir() if a.is_file()
        ]

    # SVAs (si existe)
    if ruta_svas.exists():
        resultado['svas'] = [
            a for a in ruta_svas.iterdir() if a.is_file()
        ]

    # Archivos sueltos en la raíz
    resultado['otros'] = [
        a for a in ruta.iterdir()
        if a.is_file()
        and a.parent == ruta
        and a.name not in ['0. Obligatorios', '1. SVAs']
    ]

    return resultado

def dividir_texto(texto, max_caracteres):
    palabras = texto.split()
    numero_lineas=0

    if not palabras:
        return ""

    resultado = palabras[0]
    longitud_actual = len(palabras[0])

    for palabra in palabras[1:]:
        # +1 por el espacio que se agregaría
        if longitud_actual + 1 + len(palabra) <= max_caracteres:
            resultado += " " + palabra
            longitud_actual += 1 + len(palabra)
        else:
            resultado += "\n" + palabra
            longitud_actual = len(palabra)
            numero_lineas+=1

    return resultado, numero_lineas
