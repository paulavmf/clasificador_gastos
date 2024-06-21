import pdfplumber
import pandas as pd
import re

def extract_text_from_pdf(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            text.append(pagina.extract_text())
        return '\n'.join(text)

def process_text_to_pdf(text):
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

    # Descripción y valores numéricos
    # descripcion_partes = partes[1].split()
    # Inicializar variables para cargos, abonos y saldo
    saldo = rest_of_line.split()[-1]
    cargo_abono = rest_of_line.split()[-2]
    description = rest_of_line.replace(' '.join([cargo_abono, saldo]), '').strip()
    return [fecha, ref, fecha_valor, description, cargo_abono, saldo]


def extract_text_from_pdf_first_page(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        text.append(pdf.pages[0].extract_text())
        return '\n'.join(text)

def convert_transactions_to_df(transacciones):
    # Convierte la lista de lista transacciones a data frame
    columnas = ['Fecha', 'Ref', 'Fecha Valor', 'Descripción', 'cargos_abonos', 'Saldo']
    df = pd.DataFrame(transacciones, columns=columnas)
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', format='%d-%m-%y')
    df['Fecha Valor'] = pd.to_datetime(df['Fecha Valor'], errors='coerce', format='%d-%m-%y')
    # Convertir las columnas de importe a numérico
    return df


def parse_pdf_text(text: str, separador):
    #desde el texto plano del pdf parsea a la lista con cada campo
    lineas = text.split('\n')

    # Filtrar las líneas relevantes
    transacciones = []
    for linea in lineas:
        # Asumir que cada línea relevante contiene una fecha en el formato dd-mm-yy
        if "-24 " in linea:  # Ajusta esto según tu formato de fecha
            transacciones.append(separador(linea))



