import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Crear el gráfico de quesos según el Tipo de Comercio
def crear_grafico_quesos(df):
    tipo_comercio_counts = df['Type'].value_counts()
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


def bar_plot_by_category_from_multy_sheets(df, category):
    # Cambiar el signo de todos los valores en la columna 'IMPORTE'
    df.loc[:, 'IMPORTE'] = df['IMPORTE'] * -1
    # Filtrar las filas donde el Tipo de Comercio es la categoría especificada
    df_filtered = df[df['Tipo de Comercio'] == category].copy()
    # Asegurarse de que la columna 'FECHA' sea de tipo datetime
    df_filtered.loc[:, 'FECHA'] = pd.to_datetime(df_filtered['FECHA'])

    # Crear una columna adicional para el mes y año
    df_filtered['Mes-Año'] = df_filtered['FECHA'].dt.to_period('M')
    # Agrupar los datos por Mes-Año y sumar los importes
    df_agrupado = df_filtered.groupby('Mes-Año')['IMPORTE'].sum()

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    df_agrupado.plot(kind='bar', color='blue')
    plt.xlabel('Mes')
    plt.ylabel(f'Total Gasto en {category} (€)')
    plt.title(f'Gasto Mensual en la Categoría "{category}"')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()





def create_multy_bar_diagram(df, stack = False):
    # Asegurarse de que la columna 'FECHA' sea de tipo datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # df.loc[:, 'cargo'] = df['IMPORTE'] * -1

    # Crear una columna adicional para el mes y año
    df.loc[:, 'Mes-Año'] = df['Fecha'].dt.to_period('M')

    # Agrupar los datos por mes y tipo de comercio y sumar los importes
    df_agrupado = df.groupby(['Mes-Año', 'Type'])['cargo'].sum().unstack().fillna(0)

    # Crear el diagrama de barras
    df_agrupado.plot(kind='bar', stacked=stack, figsize=(12, 8))

    # Configurar el título y las etiquetas
    plt.title('Gasto en Tipos de Comercio por Mes')
    plt.xlabel('Mes-Año')
    plt.ylabel('Gasto Total (€)')
    plt.xticks(rotation=45)
    plt.legend(title='Tipo de Comercio')
    plt.tight_layout()

    # Mostrar el diagrama de barras
    plt.show()
