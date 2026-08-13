"""
Datos y mapas de coordenadas para los contratos de On Empresas / On Negocios.

Los archivos de plantillas viven en:
    RUTA_CONTRATOS / ... / "0. Obligatorios" / <archivo>

Los anexos de Internet (xlsx) tienen una hoja llamada "Recurrente mensual"
con coordenadas fijas independientemente del plan (199, 249, 349, etc.).
"""

from pathlib import Path

from src.datosEntel import (
    HC_ARCHIVO_POR_PLAN,
    HC_COORDS_POR_PLAN,
)


HOJA_RECORRENTE = 'Recurrente mensual'
PREFIJO_ANEXO_INTERNET = 'ANEXO - Internet'


def coordenadas_anexo_internet(ruta_plantilla: Path) -> dict:
    """
    Devuelve el mapa de coordenadas si el archivo es un anexo de
    Internet de On Empresas, o {} si no aplica.
    """
    if not ruta_plantilla.name.startswith(PREFIJO_ANEXO_INTERNET):
        return {}
    if not ruta_plantilla.suffix.lower() in ('.xlsx', '.xlsm'):
        return {}
    return {
        'DIA':          (HOJA_RECORRENTE, 'D69'),
        'NOMBRE_MES':   (HOJA_RECORRENTE, 'E69'),
        'ANIO':         (HOJA_RECORRENTE, 'G69'),
        'RRLL':         (HOJA_RECORRENTE, 'D76'),
        'CARGO':        (HOJA_RECORRENTE, 'D77'),
        'DNI':          (HOJA_RECORRENTE, 'D78'),
    }


def archivos_obligatorios(ruta_trabajo: Path) -> list[Path]:
    """Lista los archivos en '0. Obligatorios' de On Empresas."""
    ruta_oblig = ruta_trabajo / '0. Obligatorios'
    if not ruta_oblig.exists():
        return []
    return [p for p in ruta_oblig.iterdir() if p.is_file()]


__all__ = [
    'HOJA_RECORRENTE',
    'PREFIJO_ANEXO_INTERNET',
    'coordenadas_anexo_internet',
    'archivos_obligatorios',
    'HC_ARCHIVO_POR_PLAN',
    'HC_COORDS_POR_PLAN',
]
