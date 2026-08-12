import pytest
from src.generadorOnEmpresas import GeneradorOnEmpresas
from dotenv import load_dotenv
import os
from pathlib import Path


@pytest.fixture(scope="session")
def gestor():
    load_dotenv()
    base = Path(__file__).resolve().parent.parent
    excel = base / 'DATOS CORREO.xlsx'
    g = GeneradorOnEmpresas(
        os.getenv('RUTA_CLIENTES'),
        os.getenv('RUTA_CONTRATOS'),
        excel,
    )
    return g


def test_construir_ruta_trabajo(gestor):
    gestor.construir_ruta_trabajo()
    assert gestor.ruta_trabajo is not None
    assert (gestor.ruta_trabajo / '0. Obligatorios').exists()
