import pandas as pd
from IPython.display import display, HTML
import json
import os


def clasificar_transacciones(descripcion, categorias):
    for categoria, palabras_clave in categorias.items():
        if any(palabra in descripcion.lower() for palabra in palabras_clave):
            return categoria
    return 'otro'

# Función para cargar los datos de transacciones
def load_doc_transactions_bankinter(ruta_archivo):
    df = pd.read_excel(ruta_archivo, engine='xlrd', skiprows = 4).dropna( how = 'all')
    # valor a partir del cual se detiende la lectura
    stop_value = 'Total Crédito'
    # columna en la cual se encuentra el valor
    column = 'FECHA'
    # Encontrar el índice de la primera aparición del valor específico
    if stop_value in df[column].values:
        idx = df[df[column] == stop_value].index[0]
        # Crear un nuevo DataFrame con las filas hasta el índice encontrado (excluyendo las demás)
        return df.loc[:(idx-1)]
    else:
        return df

def procesar_transacciones(data, categorias):
    data['categoria'] = data['COMERCIO/CAJERO'].apply(lambda desc: clasificar_transacciones(desc, categorias))
    return data


# Crear widgets interactivos
def categories_widgets(df):
    comercios = df['COMERCIO/CAJERO'].unique().tolist()
    categorias = df['categoria'].unique().tolist() + ['otro', 'bar', 'supermercado', 'restaurante', 'transporte', 'tecnología']
    return categorias, comercios

def update_categoria(df, index, categoria):
    df.at[index, 'categoría'] = categoria
    display(df)


def clasificar_comercio(comercio, category_dict):
    for key in category_dict:
        if key.lower() in comercio.lower():
            return category_dict[key]
    return 'otros'

def get_categories_from_df(df) -> list:
    categories = df['Tipo de Comercio'].unique().tolist()
    return categories

def filter_df_by_category(df, category_name):
    return df[df['Tipo de Comercio'] == category_name]

def listar_archivos_en_carpeta(carpeta):
    archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
    archivos_paths = [os.path.join(carpeta, f) for f in archivos]
    return archivos, archivos_paths


# Función para guardar el DataFrame en un archivo Excel y concatenar DataFrames adicionales
def save_df_by_dates(df_nuevo, archivo='mis_gastos.xlsx'):
    # Ordenar por fecha
    df_nuevo['FECHA'] = pd.to_datetime(df_nuevo['FECHA'])
    df_nuevo = df_nuevo.sort_values(by='FECHA')

    # Obtener el nombre de la hoja basado en el rango de fechas
    primera_fecha = df_nuevo['FECHA'].min().strftime('%Y-%m-%d')
    ultima_fecha = df_nuevo['FECHA'].max().strftime('%Y-%m-%d')
    hoja_nombre = f"{primera_fecha}_a_{ultima_fecha}"

    # Verificar si el archivo Excel ya existe
    if os.path.exists(archivo) and os.path.getsize(archivo) > 0:
        try:
            with pd.ExcelWriter(archivo, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_nuevo.to_excel(writer, index=False, sheet_name=hoja_nombre)
        except Exception as e:
            print(f"Error al abrir el archivo existente: {e}")
    else:
        with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
            df_nuevo.to_excel(writer, index=False, sheet_name=hoja_nombre)

    print(f'Datos guardados en la hoja: {hoja_nombre}')


def read_and_concatenate_excel(file):
    # Leer todas las hojas del archivo Excel en un diccionario de DataFrames
    df_dict = pd.read_excel(file, sheet_name=None)

    # Concatenar todos los DataFrames en uno solo
    df_concatenado = pd.concat(df_dict.values(), ignore_index=True)

    return df_concatenado

def convert_to_float(value):
    if pd.isna(value):
        return None
    elif value == 0:
        return value
    value = value.replace('.', '').replace(',', '.')  # Reemplazar ',' por '.' y eliminar '.'
    return float(value)

def save_as_csv(df, pdf_name):
    csv_name = pdf_name.replace('.pdf', '.csv')
    df.to_csv(csv_name)
