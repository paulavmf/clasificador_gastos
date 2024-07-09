import pandas as pd
from pandas import DataFrame

from src.utils.parse_pdf import *

class DataExtractor:
    def __init__(self, month, year):
        """
        :param month: Mes en español primera lentra en mayúsula
        :param year: año en cuatro dígitos
        :return: lista de transacciones cuentas corrientes
        """
        self.source = 'extractos/'
        self.month = self.validate_month(month)
        self.year = self.validate_year(year)
        self.file = f"{self.source}Extracto_{self.month}_{self.year}.pdf"
        self.movements_cuenta_corriente = DataFrame()
        self._transactions_cuenta_corriente = []
        self.movements_tarjeta = DataFrame()
        self._transactions_tarjeta = []

    @staticmethod
    def validate_month(month: str) -> str:
        valid_months = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        if month not in valid_months:
            raise ValueError(f"Mes inválido: {month}. Debe ser uno de {valid_months}.")
        return month

    @staticmethod
    def validate_year(year: int) -> int:
        if not (1900 <= year <= 2100):
            raise ValueError(f"Año inválido: {year}. Debe estar entre 1900 y 2100.")
        return year

    @property
    def transactions_cuenta_corriente(self) -> list:
        if not self._transactions_cuenta_corriente:
            self._transactions_cuenta_corriente = self._extract_transactions_cuenta_corriente()
        return self._transactions_cuenta_corriente

    @property
    def transactions_tarjeta(self) -> list:
        if not self._transactions_tarjeta:
            self._transactions_tarjeta = self._extract_transactions_tarjeta()
        return self._transactions_tarjeta

    def _extract_transactions_cuenta_corriente(self) -> list:
        text = extract_text_from_pdf_first_page(self.file)
        transacciones = parse_pdf_text(text, separar_columnas_cc)
        self._transactions_cuenta_corriente = transacciones
        return transacciones

    def _extract_transactions_tarjeta(self) -> list:
        text = extract_text_from_pdf_rest_of_pages(self.file)
        transacciones = parse_pdf_text(text, separar_columnas_tajeta)
        self._transactions_tarjeta = transacciones
        return transacciones

    def convert_transactions_cuenta_corriente_to_dataframe(self) -> DataFrame:
        df = convert_transactions_to_df(self.transactions_cuenta_corriente)
        self.movements_cuenta_corriente = df
        return df

    def convert_transactions_tarjeta_to_dataframe(self) -> DataFrame:
        df = convert_transactions_tarjeta_to_df(self.transactions_tarjeta)
        self.movements_tarjeta = df
        return df

    def extraer(self):
        self.convert_transactions_cuenta_corriente_to_dataframe()
        self.convert_transactions_tarjeta_to_dataframe()














