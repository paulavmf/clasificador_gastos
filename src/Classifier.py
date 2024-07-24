import json

import pandas as pd

from src.Dataloader import DataLoader
import sqlite3


class Classifier:
    def __init__(self, dataloader: DataLoader, categories_file):
        self.categories = json.load(open(categories_file))
        self.file = dataloader.file
        self.classified_df = pd.DataFrame()
        self.db = dataloader.db
        self.table = dataloader.table

    # Función para clasificar el comercio
    def classify_description(self, description):
        for key in self.categories:
            if key.lower() in description.lower():
                return self.categories[key]
        return 'otros'

    def classify_new_file(self):
        df = pd.read_csv(self.file)
        df['Type'] = df['Descripción'].apply(lambda x: self.classify_description(x))
        self.classified_df = pd.concat([self.classified_df, df], ignore_index=True)
        return self.classified_df

    def update_classification_in_sqlite3(self):
        conn = sqlite3.connect('cuentas.db')
        df = pd.read_sql_query(f"SELECT * FROM {self.table}", conn)
        df['Type'] = df['Descripción'].apply(lambda x: self.classify_description(x))
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {self.table}")
        df.to_sql(self.table, conn, if_exists='append', index=False)
        conn.close()
