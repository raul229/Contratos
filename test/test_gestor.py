import pytest
from src.gestorContratos import GestorContratos
from dotenv import  load_dotenv
import os


@pytest.fixture(scope="session")
def gestor():
    load_dotenv()
    g = GestorContratos(os.getenv('RUTA_CLIENTES'), os.getenv('RUTA_CONTRATOS'))
    return g


def test_construir_ruta_trabajo(gestor):
    gestor.construir_ruta_trabajo()
    assert True
