from pathlib import Path

import pytest

fitz = pytest.importorskip('fitz', exc_type=ImportError)
from src.generadorEntel import GeneradorEntel


def test_llena_pdf_pack_empresas():
    """Genera un PDF de muestra persistente para revisar coordenadas."""
    raiz = Path(__file__).resolve().parent.parent
    plantilla = raiz / 'CONTRATOS_ENTEL' / 'pack empresas.pdf'
    carpeta_cliente = raiz / 'test' / 'salidas' / 'CLIENTE-20123456789'
    editables = carpeta_cliente / 'EDITABLES'
    editables.mkdir(parents=True, exist_ok=True)

    generador = GeneradorEntel(raiz / 'test' / 'salidas', raiz / 'CONTRATOS_ENTEL')
    generador.contexto = {
        'RAZON_SOCIAL': 'EMPRESA PACK DE PRUEBA S.A.C.',
        'RUC': '20123456789',
        'RRLL': 'ANA PRUEBA LOPEZ',
        'TIPO_DOCUMENTO_RRLL': 'DNI',
        'DNI': '12345678',
        'CORREO_RRLL': 'ana.prueba@example.com',
        'CELULAR_RRLL': '999888777',
        'DOMICILIO_INSTALACION': 'Av. Prueba 123, Lima',
        'FECHA': '13/08/2026',
        'DIA': '13',
        'NOMBRE_MES': 'Agosto',
        'ANIO': '2026',
        'DOMICILIO_INSTALACION_2': 'Av. Prueba 123, Lima',
        'NUMERO_FIJO': '854785789',
    }
    generador.nombre_plan = 'Pack Empresas'
    generador.velocidad = 300
    generador.promocion = 'Solo 30% por 6m.'
    generador.renta_fija = '129.9'
    generador.descuento_segun_plan = '33.03'
    generador.carpeta_cliente = carpeta_cliente
    generador.editables_cliente = editables

    generador._llenar_un_pdf(plantilla)

    resultado = carpeta_cliente / 'pack empresas - prueba.pdf'
    (carpeta_cliente / plantilla.name).replace(resultado)
    assert resultado.is_file()

    with fitz.open(resultado) as pdf:
        texto_pagina_1 = pdf[0].get_text()
        texto_pagina_3 = pdf[2].get_text()
        texto_pagina_5 = pdf[4].get_text()

    assert 'EMPRESA PACK DE PRUEBA S.A.C.' in texto_pagina_1
    assert '20123456789' in texto_pagina_1
    assert 'Pack Empresas 300' in texto_pagina_1
    assert '129.9' in texto_pagina_1
    assert 'ANA PRUEBA LOPEZ' in texto_pagina_3
    assert '13/08/2026' in texto_pagina_3
    assert '999888777' in texto_pagina_5
