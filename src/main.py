from src.Transformer import DataTransformer
from src.Extractor import DataExtractor
from src.Dataloader import DataLoader
import os

DATA_FOLDER = "/home/paula/Documentos/clasificador_gastos/extractos"

# TODO hay que corregir cosas xq Septiembre , octubre... no está funcionando

def update_data():
    years = [2023 , 2024]
    months = ["Enero", "Febrero", "Marzo",
              "Abril", "Mayo", "Junio", "Julio",
              "Agosto", "Septiembre", "Octubre",
              "Noviembre", "Diciembre"]
    for year in years:
        for month in months:
            if os.path.exists(os.path.join(DATA_FOLDER, f"Extracto_{month}_{year}.pdf")):
                extractor = DataExtractor(month, year)
                extractor.extraer()
                transformer = DataTransformer(extractor)
                transformer.convert_all_movements_to_dataframe()
                transformer.save_as_csv()
                loader = DataLoader(transformer)
                # TODO solo aparece la ultima fila en el sqlite3 hay que mejorar el control de movimientos únicos
                # loader.load_data_in_db()



if __name__ == '__main__':
    update_data()

