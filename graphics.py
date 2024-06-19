import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Crear el gráfico de quesos según el Tipo de Comercio
def crear_grafico_quesos(df):
    tipo_comercio_counts = df['Tipo de Comercio'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(tipo_comercio_counts, labels=tipo_comercio_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribución de Gastos por Tipo de Comercio')
    plt.show()

# Crear la línea temporal de gasto en porcentaje
def crear_linea_temporal(df, category = None):
    df['Fecha'] = pd.to_datetime(df['FECHA']).copy()
    df.set_index('Fecha', inplace=True)
    monthly_expenses = - df['IMPORTE'].cumsum()
    total_expense = - df['IMPORTE'].cumsum().iloc[-1]
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_expenses)
    title = 'total gastado mensual {}'.format(total_expense)
    if category:
        title = '{} gastado mensual en {}'.format(total_expense, category)
    plt.title(title)
    plt.xlabel('Fecha')
    plt.ylabel('Gasto acumulado')
    plt.show()


def bar_plot_by_category_from_multy_sheets(dfs,category):
# Inicializar un diccionario para almacenar los gastos por mes
    monthly_expenses = {}
    for sheet_name, df in dfs.items():
        # Filtrar las filas donde el Tipo de Comercio es "bar"
        selection_expenses = df[df['Tipo de Comercio'] == category]
        # Calcular el gasto total para este mes
        selection_expenses.loc[:, 'IMPORTE'] = selection_expenses['IMPORTE'] * -1
        total_bar_expenses = selection_expenses['IMPORTE'].sum()
        # Almacenar el resultado en el diccionario
        monthly_expenses[sheet_name] = total_bar_expenses

    # Convertir el diccionario a un DataFrame para facilitar la visualización
    monthly_bar_expenses_df = pd.DataFrame.from_dict(monthly_expenses, orient='index',
                                                     columns=[f'Total Gasto en {category}'])
    monthly_bar_expenses_df.index.name = 'Mes'
    monthly_bar_expenses_df.reset_index(inplace=True)

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(monthly_bar_expenses_df['Mes'], monthly_bar_expenses_df[f'Total Gasto en {category}'], color='blue')
    plt.xlabel('Mes')
    plt.ylabel(f'Total Gasto en {category} (€)')
    plt.title(f'Gasto Mensual en la Categoría "{category}"')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
