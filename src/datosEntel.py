"""
Datos y mapas de coordenadas para los contratos de Entel.

Estructura:
- PLANES_ENTEL: tarifas por plan y velocidad.
- COORDS_ENTEL_PAGINA_*: mapas de coordenadas por página lógica.

Cada mapa tiene la forma:
    {nombre_campo: (x, y, opciones)}

Opciones disponibles:
    - 'value'          texto fijo que se imprime literalmente
    - 'field'          nombre real del dato (default: el nombre del campo)
    - 'transform'      función nombrada que produce el texto
    - 'tamano'         tamaño de fuente (default 12)
    - 'max_caracteres' si está presente, divide el texto en varias líneas

Resolución de un valor (en `GeneradorEntel._resolver_valor`):
    1. 'value' literal
    2. 'transform' aplicado al contexto + datos del generador
    3. campo del contexto del cliente (JSON)
    4. campo de los datos del generador (plan, renta, etc.)
"""

PLANES_ENTEL = {
    'Internet Empresas': {
        200: {'renta': 90.00, 'descuento': 22.88},
        300: {'renta': 120.00, 'descuento': 30.51},
        500: {'renta': 150.00, 'descuento': 38.14},
        1000: {'renta': 180.00, 'descuento': 45.76},
    },
    'Pack Empresas': {
        200: {'renta': 99.90, 'descuento': 25.40},
        300: {'renta': 129.90, 'descuento': 33.03},
        500: {'renta': 159.90, 'descuento': 40.65},
        1000: {'renta': 189.90, 'descuento': 48.28},
    },
}


# --------------------------------------------------
# MAPAS DE COORDENADAS POR PÁGINA LÓGICA
# --------------------------------------------------

COORDS_ENTEL_PAGINA_1: dict[str, tuple[int, int, dict]] = {
    'RAZON_SOCIAL':          (20, 260, {'tamano': 9, 'max_caracteres': 40}),
    'RUC':                   (50, 295, {}),
    'RRLL':                  (20, 350, {'max_caracteres': 40}),
    'DOCUMENTO_Y_DNI':       (25, 400, {'transform': 'doc_y_dni'}),
    'CORREO_RRLL':           (25, 430, {}),
    'CELULAR_RRLL':          (25, 460, {}),
    'DOMICILIO_INSTALACION': (20, 513, {'max_caracteres': 60, 'tamano': 8}),
    'DOMICILIO_INSTALACION_2': (20, 563, {'max_caracteres': 60, 'tamano': 8}),
    'VELOCIDADES':           (330, 440, {'transform': 'velocidades'}),
    'RUC_2':                 (110, 610, {'field': 'RUC'}),
    'NOMBRE_PLAN':           (140, 625, {'transform': 'nombre_plan'}),
    'PROMOCION':             (140, 640, {'field': '_PROMOCION'}),
    'CHECK_SERVICIO_NUEVO':  (25, 665, {'value': 'X'}),
    'RENTA_FIJA':            (243, 712, {'field': '_RENTA_FIJA'}),
}

COORDS_ENTEL_PAGINA_3: dict[str, tuple[int, int, dict]] = {
    'RRLL':  (195, 300, {'max_caracteres': 17}),
    'CARGO': (195, 330, {'value': 'GERENTE GENERAL'}),
    'FECHA': (60, 345, {}),
    'HORA':  (220, 345, {'value': '10 : 00 : 00'}),
}

COORDS_ENTEL_PAGINA_5: dict[str, tuple[int, int, dict]] = {
    'RRLL':         (40, 510, {'max_caracteres': 17}),
    'DNI':          (180, 510, {}),
    'CARGO':        (260, 498, {'value': 'GERENTE\nGENERAL'}),
    'CELULAR_RRLL': (350, 510, {'max_caracteres': 10}),
    'CORREO_RRLL':  (436, 510, {'tamano': 9, 'max_caracteres': 27}),
    'DIA_MES_ANIO': (200, 640, {'transform': 'dia_mes_anio'}),
    'RRLL_2':       (90, 710, {'field': 'RRLL', 'tamano': 10}),
    'CARGO_2':      (100, 730, {'value': 'GERENTE GENERAL'}),
}

COORDS_ENTEL_PAGINA_6: dict[str, tuple[int, int, dict]] = {
    'FECHA':                 (120, 185, {}),
    'RUC':                   (230, 215, {}),
    'RAZON_SOCIAL':          (225, 240, {'max_caracteres': 50, 'tamano': 10}),
    'RRLL':                  (230, 260, {'tamano': 10}),
    'CELULAR_RRLL':          (230, 280, {'tamano': 10}),
    'DOMICILIO_INSTALACION': (80, 340, {'max_caracteres': 70, 'tamano': 12}),
}

COORDS_ENTEL_PAGINA_7: dict[str, tuple[int, int, dict]] = {
    'FECHA':                 (120, 185, {}),
    'RUC':                   (230, 225, {}),
    'RAZON_SOCIAL':          (225, 248, {'max_caracteres': 50, 'tamano': 10}),
    'RRLL':                  (230, 270, {'tamano': 10}),
    'CELULAR_RRLL':          (230, 290, {'tamano': 10}),
    'DOMICILIO_INSTALACION': (80, 350, {'max_caracteres': 70, 'tamano': 12}),
    'DESCUENTO':             (230, 430, {'transform': 'descuento'}),
}


# --------------------------------------------------
# MAPAS POR ARCHIVO PDF
# --------------------------------------------------
# {nombre_archivo_pdf: {num_pagina_fisica: mapa_de_coordenadas}}
#
# Caso A — un solo PDF con 7 páginas (estado actual):
#     'arrendamiento-...pdf' -> {0: P1, 2: P3, 4: P5, 5: P6, 6: P7}
#
# Caso B — PDFs separados (5 + 2):
#     'arrendamiento-...pdf' -> {0: P1, 2: P3, 4: P5}
#     'anexo-...pdf'         -> {0: P6, 1: P7}  # reindexar a 0

MAPA_ENTEL_POR_ARCHIVO: dict[str, dict[int, dict]] = {
    'contratos.pdf': {
        0: COORDS_ENTEL_PAGINA_1,
        2: COORDS_ENTEL_PAGINA_3,
        4: COORDS_ENTEL_PAGINA_5,
        # 5: COORDS_ENTEL_PAGINA_6,
        # 6: COORDS_ENTEL_PAGINA_7,
    },
    # Cuando el contrato se divida, registrar aquí el nuevo archivo:
    'bono duplica.pdf': {
        0: COORDS_ENTEL_PAGINA_6,
        # 1: COORDS_ENTEL_PAGINA_7,
    },
    'promocion 30 x 6 meses.pdf': {
        # 0: COORDS_ENTEL_PAGINA_6,
        0: COORDS_ENTEL_PAGINA_7,
    },
}
