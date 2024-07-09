import pandas as pd
from pandas import DataFrame

from src.Extractor import DataExtractor
from src.utils.analyze import correct_and_merge_cc_t

class DataTransformer:
    def __init__(self, extractor: DataExtractor):
        self.file = extractor.file
        self.data_cuenta_corriente = extractor.movements_cuenta_corriente
        self.data_tarjeta = extractor.movements_tarjeta
        self.all_monthly_movements = DataFrame()

    def convert_all_movements_to_dataframe(self) -> DataFrame:
        df = correct_and_merge_cc_t(self.data_cuenta_corriente, self.data_tarjeta)
        self.all_monthly_movements = df
        return df

    def save_as_csv(self):
        csv_name = self.file.replace('.pdf', '.csv')
        self.all_monthly_movements.to_csv(csv_name)

    def save_and_transform(self):
        self.convert_all_movements_to_dataframe()
        self.save_as_csv()
