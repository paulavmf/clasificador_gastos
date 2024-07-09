import pandas as pd
from pandas import DataFrame
import os
from src.Extractor import DataExtractor
from src.utils.analyze import correct_and_merge_cc_t, add_initial_saldo_col

class DataTransformer:
    def __init__(self, extractor: DataExtractor):
        self.file = extractor.file
        self.data_cuenta_corriente = extractor.movements_cuenta_corriente
        self.data_tarjeta = extractor.movements_tarjeta
        self.all_monthly_movements = DataFrame()

    def convert_all_movements_to_dataframe(self) -> DataFrame:
        df = correct_and_merge_cc_t(self.data_cuenta_corriente, self.data_tarjeta)
        df = add_initial_saldo_col(df, self.data_cuenta_corriente)
        self.all_monthly_movements = df
        return df

    def save_as_csv(self):
        csv_name = self.file.replace('.pdf', '.csv')
        if os.path.exists(csv_name):
            print(f'File {csv_name} already exists it will be overwritten')
        self.all_monthly_movements.to_csv(csv_name)
