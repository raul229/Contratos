import os
from pathlib import Path

from src.generadorContratos import GeneradorContratos
from src.generadorEntel import GeneradorEntel
from src.generadorOnEmpresas import GeneradorOnEmpresas
from utilidades.utils import mostrar_opciones


def construir_generador(
    operador: str,
    base_dir: Path,
) -> GeneradorContratos:
    """
    Fábrica simple que devuelve el generador adecuado según el operador.
    """
    carpeta_clientes = Path(os.getenv('RUTA_CLIENTES'))
    if operador == 'Entel':
        carpeta_contratos = Path(os.getenv('CONTRATOS_ENTEL'))
        carpeta_clientes_entel = Path(os.getenv('RUTA_CLIENTES_ENTEL'))
        return GeneradorEntel(carpeta_clientes_entel, carpeta_contratos)

    if operador == 'On Empresas':
        carpeta_contratos = Path(os.getenv('RUTA_CONTRATOS'))
        excel_correo = base_dir / 'DATOS CORREO.xlsx'
        return GeneradorOnEmpresas(carpeta_clientes, carpeta_contratos, excel_correo)

    raise ValueError(f'Operador no soportado: {operador}')


def elegir_operador() -> str:
    return mostrar_opciones(['Entel', 'On Empresas'])
