from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from subprocess import run, DEVNULL
from datetime import datetime


def convertir_a_pdf(ruta_origen: Path, sistema_operativo: str) -> Path | None:
    """
    Convierte un archivo (docx/xlsx/xlsm) a PDF con LibreOffice en Linux
    o con docx2pdf en Windows. Devuelve la ruta del PDF generado.
    """
    if sistema_operativo == 'Linux':
        carpeta_salida = ruta_origen.parent
        run(
            [
                'libreoffice',
                '--headless',
                '--convert-to',
                'pdf',
                '--outdir',
                str(carpeta_salida),
                str(ruta_origen),
            ],
            check=True,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        return carpeta_salida / (ruta_origen.stem + '.pdf')

    from docx2pdf import convert
    if ruta_origen.suffix != '.docx':
        raise ValueError('En Windows solo se convierten archivos .docx')
    destino = ruta_origen.parent / (ruta_origen.stem + '.pdf')
    convert(str(ruta_origen), str(destino))
    return destino


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

def completar_fechas(contexto:dict)->dict:
     # completado automatico de fecha
    meses = {
        '01': 'Enero',
        '02': 'Febrero',
        '03': 'Marzo',
        '04': 'Abril',
        '05': 'Mayo',
        '06': 'Junio',
        '07': 'Julio',
        '08': 'Agosto',
        '09': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre',
    }

    fecha = contexto.get('FECHA') or datetime.now().strftime('%d/%m/%Y')
    dia, mes, anio = fecha.split('/')

    contexto.update({
        'FECHA': fecha,
        'DIA': dia,
        'MES': mes,
        'NOMBRE_MES': meses.get(mes, ''),
        'ANIO': anio,
    })
    
    return contexto

def _completar_datos_entel(contexto:dict)->dict:


    return contexto


# --------------------------------------------------
# CORREO (.eml)
# --------------------------------------------------

def generar_eml(
    plantilla: Path,
    contexto: dict,
    adjuntos: list[Path],
    carpeta_destino: Path,
) -> Path:
    """
    Renderiza una plantilla .eml con Jinja2 y la guarda en
    `carpeta_destino`. La plantilla debe tener bloques Jinja
    para: subject, from, to, cc, bcc, body.

    Ejemplo de plantilla:
        subject: Contrato {{RAZON_SOCIAL}}
        from: ventas@empresa.com
        to: {{CORREO_RRLL}}
        cc: {% if CORREO_ADMINISTRATIVO %}{{CORREO_ADMINISTRATIVO}}{% endif %}
        bcc:
        body: |
            Estimado {{RRLL}},
            Adjuntamos su contrato.
    """
    from jinja2 import Environment, FileSystemLoader, StrictUndefined

    env = Environment(
        loader=FileSystemLoader(str(plantilla.parent)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    template = env.get_template(plantilla.name)
    rendered = template.render(**contexto)

    metadata = _parsear_eml_plantilla(rendered)
    msg = EmailMessage()
    msg['Subject'] = metadata['subject']
    msg['From'] = metadata['from']
    msg['To'] = metadata['to']
    if metadata.get('cc'):
        msg['Cc'] = metadata['cc']
    if metadata.get('bcc'):
        msg['Bcc'] = metadata['bcc']
    msg.set_content(metadata['body'])

    for ruta_adj in adjuntos:
        ruta_adj = Path(ruta_adj)
        if not ruta_adj.exists():
            continue
        msg.add_attachment(
            ruta_adj.read_bytes(),
            maintype='application',
            subtype='octet-stream',
            filename=ruta_adj.name,
        )

    carpeta_destino.mkdir(parents=True, exist_ok=True)
    nombre = f"correo_{contexto.get('RUC', 'cliente')}.eml"
    salida = carpeta_destino / nombre
    salida.write_bytes(bytes(msg))
    return salida


def _parsear_eml_plantilla(rendered: str) -> dict:
    """
    Parsea el texto renderizado en bloques:
        subject: ...
        from: ...
        to: ...
        cc: ...
        bcc: ...
        body: |
            ...
    """
    campos = {'subject', 'from', 'to', 'cc', 'bcc', 'body'}
    metadata: dict = {c: '' for c in campos}

    lineas = rendered.splitlines()
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        match = next(
            (c for c in campos if linea.startswith(f'{c}:')),
            None,
        )
        if match is None:
            i += 1
            continue
        _, _, valor_inicial = linea.partition(':')
        valor = valor_inicial.strip()

        # body: | inicia un bloque multilínea
        if match == 'body' and '|' in valor_inicial:
            i += 1
            bloque = []
            while i < len(lineas) and (
                lineas[i].startswith('    ')
                or lineas[i].startswith('\t')
                or lineas[i] == ''
            ):
                bloque.append(lineas[i].lstrip())
                i += 1
            metadata['body'] = '\n'.join(bloque).strip()
            break

        # valor en una sola línea (puede continuar en líneas con indentación)
        i += 1
        while i < len(lineas) and (
            lineas[i].startswith('    ') or lineas[i].startswith('\t')
        ):
            valor += ' ' + lineas[i].strip()
            i += 1
        metadata[match] = valor

    return metadata
