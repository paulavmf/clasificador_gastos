import pandas as pd
from IPython.display import display, HTML
import json


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

