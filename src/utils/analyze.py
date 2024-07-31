import pandas as pd
from src.utils.helpers import convert_to_float

def correct_cc_df(df):
    # sustrae el cargo por el recibo de la tarjeta y
    df = df[df['Descripción'] !='RECIBO PLATINUM']
    df = df.drop(columns=['Ref', 'Fecha Valor', 'Saldo'])
    return df



def correct_and_merge_cc_t(df_cc, df_t):
    df_cc = correct_cc_df(df_cc)
    df_cc['Fecha'] = pd.to_datetime(df_cc['Fecha'], format='%d/%m/%Y')
    df_t['Fecha'] = pd.to_datetime(df_t['Fecha'], format='%d/%m/%Y')
    df = pd.concat([df_cc, df_t])
    df = df.sort_values(by='Fecha').reset_index(drop=True)
    return df

def initial_saldo(df_cc):
    # take initial saldo from cuenta after discount recibo platinum

    def find_platinum_index(df_cc):
        index_list = df_cc.index[df_cc['Descripción'] == 'RECIBO PLATINUM'].tolist()
        index = max(index_list)
        return index
    platinum_index = find_platinum_index(df_cc)
    saldo = convert_to_float(df_cc.loc[platinum_index, 'Saldo'])
    return saldo

def add_saldo(df, saldo_inicial):
    df['Saldo'] = 0
    for i in range(len(df)):
        if i == 0:
            df.loc[i, 'Saldo'] = saldo_inicial
        else:
            df.loc[i, 'Saldo'] = df.loc[i - 1, 'Saldo'] - df.loc[i, 'cargo'] + df.loc[i, 'abono']

    return df



def add_initial_saldo_col(df, df_cc):
    saldo = initial_saldo(df_cc)
    return add_saldo(df,saldo)




