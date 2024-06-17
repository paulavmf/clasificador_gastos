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


