from pathlib import Path


def generar_opciones(ruta:str|Path)->list:
    ruta = Path(ruta)
    if not ruta.is_dir():
        return []
    return [p.name for p in ruta.iterdir()]

def mostrat_opciones(lita_opciones:list[str]):
    print('Puedes escoger entre los siguientes planes: ')
    for index,  opcion in enumerate(lita_opciones):
        print(index, '-', opcion)
    respuesta =int(input('Respuesta: '))
    return lita_opciones[respuesta]
