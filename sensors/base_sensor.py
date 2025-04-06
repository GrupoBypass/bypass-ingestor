import pandas as pd

class BaseSensor:
    def __init__(self, sensor_name: str):
        self.sensor_name = sensor_name

    def generate_data(self) -> pd.DataFrame:
        """Método para gerar os dados específicos de cada sensor"""
        raise NotImplementedError

    def get_output_path(self) -> str:
        """Caminho da pasta referência de cada sensor que vamos salvar no lakehouse"""
        raise NotImplementedError