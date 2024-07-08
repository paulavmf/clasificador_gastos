import pdfplumber
import pandas as pd
import re

# CONVIERTO EL PDF EN TEXTO PLANO
def extract_text_from_pdf(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            text.append(pagina.extract_text())
        return '\n'.join(text)

def extract_text_from_pdf_first_page(pdf_path):
    # TODO cuento con que los movimientos de cuetna está todos en una misma página
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        text.append(pdf.pages[0].extract_text())
        return '\n'.join(text)

def extract_text_from_pdf_rest_of_pages(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in range(1, len(pdf.pages)):
            text.append(pdf.pages[page].extract_text())
        return '\n'.join(text)

def process_text_to_df(text):
    lines = text.split('\n')
    transactions = []
    for line in lines:
        if "-24 " in line:  # Ajusta esto según tu formato de fecha
            transactions.append(line.split(','))
        # Crear un DataFrame
    columnas = ['Fecha', 'Descripción', 'Movimiento', 'Importe']
    df = pd.DataFrame(transactions, columns=columnas)

    # Convertir la columna de fecha a formato datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    # Convertir la columna de importe a numérico
    df['Importe'] = pd.to_numeric(df['Importe'], errors='coerce')
    return df


def separar_columnas_cc(linea):
    # separa las columnas de la primera página del extracto, la parte de cuenta corriente
    partes = re.split(r'\s{2,}', linea)

    # Fechas y Ref
    fecha = partes[0].split()[0]
    ref = partes[0].split()[1]
    fecha_valor = partes[0].split()[2]

    rest_of_line = linea.replace(' '.join([fecha, ref, fecha_valor]), '').strip()
    saldo = rest_of_line.split()[-1]
    cargo_abono = rest_of_line.split()[-2]
    description = rest_of_line.replace(' '.join([cargo_abono, saldo]), '').strip()
    cargo = cargo_abono
    abono = None
    if parse_abonos(description):
        cargo = None
        abono = cargo_abono
    return [fecha, ref, fecha_valor, description, cargo, abono, saldo]

def separar_columnas_tajeta(linea):
    # separa las columnas de la primera página del extracto, la parte de cuenta corriente
    # TODO MEJORAR porque cuenta con que todos son cargos y con que la columna Referencia siembre está vacía
    partes = re.split(r'\s{2,}', linea)
    # Fechas y Ref
    fecha = partes[0].split()[0]
    rest_of_line = linea.replace(' '.join([fecha]), '').strip()
    cargo_abono = rest_of_line.split()[-1]
    descripcion = rest_of_line.replace(' '.join([cargo_abono]), '').strip()
    cargo = cargo_abono
    abono = None
    if parse_abonos(descripcion):
        cargo = None
        abono = cargo_abono
    return [fecha, descripcion, cargo, abono]

def convert_transactions_to_df(transacciones):
    # Convierte la lista de lista transacciones a data frame
    columnas = ['Fecha', 'Ref', 'Fecha Valor', 'Descripción', 'cargo', 'abono', 'Saldo']
    df = pd.DataFrame(transacciones, columns=columnas)
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', format='%d-%m-%y')
    df['Fecha Valor'] = pd.to_datetime(df['Fecha Valor'], errors='coerce', format='%d-%m-%y')
    # Convertir las columnas de importe a numérico
    return df

def convert_transactions_tarjeta_to_df(transacciones):
    # Convierte la lista de lista transacciones a data frame
    columnas = ['Fecha', 'Descripción', 'cargo', 'abono']
    df = pd.DataFrame(transacciones, columns=columnas)
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', format='%d-%m-%y')
    # Convertir las columnas de importe a numérico
    return df


def parse_pdf_text(text: str, separador_columnas):
    #desde el texto plano del pdf parsea a la lista con cada campo
    lineas = text.split('\n')

    # Filtrar las líneas relevantes
    transacciones = []
    for linea in lineas:
        # Asumir que cada línea relevante contiene una fecha en el formato dd-mm-yy
        if "-24 " in linea:  # Ajusta esto según tu formato de fecha
            transacciones.append(separador_columnas(linea))
    return transacciones


def parse_abonos(text):
    if "TRANSF " in text:
        return True
    elif "PAGO BIZUM DE " in text:
        return True
    else:
        return False




