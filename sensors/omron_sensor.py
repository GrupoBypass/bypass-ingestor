import os
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from datetime import datetime, timedelta
from sensors.base_sensor import BaseSensor

class SensorOmron(BaseSensor):
    def __init__(self):
        super().__init__("Omron")
        self.x = 50
        self.y = 50
        self.matriz = []

    def generate_data(self) -> pd.DataFrame:
        dados_simulados = []
        
        df = pd.DataFrame( self._get_random_data(self.x, self.y, self.matriz))
        return df

    def _get_random_data(self, x, y, matrizFinal):
        for i in range(x):
            linha = []
            for j in range(y):
                valor = random.randint(0, 1)
                linha.append(valor)
            matrizFinal.append(linha)

        for i in range(x):
            linha = []
            for j in range(y):
                print(matrizFinal[i][j], end="  ")
            print()
        
        return matrizFinal

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"/data/{self.sensor_name}/{today}"

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)

