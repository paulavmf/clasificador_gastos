import sqlite3
import pandas as pd
from src.Transformer import DataTransformer
import os

# TODO falta controlar que no repitan

DB_DIRECTORY = "/home/paula/Documentos/clasificador_gastos/"
class DataLoader:
    def __init__(self, transformer: DataTransformer):
        self.file = transformer.file
        self.data = self.add_file_col(transformer.all_monthly_movements, transformer.file)
        self.db = "cuenta.db"

    @staticmethod
    def add_file_col(df: pd.DataFrame, file) -> pd.DataFrame:
        df["source_file"] = file
        return df

    def load_data_in_db(self):
        df = self.data
        conn = sqlite3.connect(os.path.join(DB_DIRECTORY, self.db))
        df.to_sql('movements', conn, if_exists='replace')



