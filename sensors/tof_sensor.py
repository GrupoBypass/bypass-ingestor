import os
import numpy as np
import pandas as pd

from datetime import datetime, time

from sensors.base_sensor import BaseSensor

class SensorToF(BaseSensor):
    def __init__(self):
        super().__init__("tof")

        # Dimensões físicas do vagão (em metros)
        self.comprimento_m = 20.0
        self.largura_m = 2.8
        self.altura_m = 2.5

        # Resolução do voxel (tamanho de cada cubo em metros)
        self.resolucao_voxel_m = {
            'z': 0.25,  # altura
            'y': 0.10,  # largura
            'x': 0.20   # comprimento
        }

        # Cálculo das dimensões da matriz 3D
        self.dim_z = int(self.altura_m / self.resolucao_voxel_m['z'])    # 10 camadas
        self.dim_y = int(self.largura_m / self.resolucao_voxel_m['y'])   # 28 colunas
        self.dim_x = int(self.comprimento_m / self.resolucao_voxel_m['x']) # 100 linhas

    def generate_data(self) -> pd.DataFrame:
        """
        Simula a captura de uma matriz ToF e retorna um DataFrame com timestamp e profundidade.
        Em horários de pico, simula maior ocupação (menor distância ao teto).
        """
        now = datetime.now()
        horario_atual = now.time()

        # Definir se estamos em horário de pico
        em_horario_pico = (
            time(6, 0) <= horario_atual <= time(9, 0) or
            time(17, 0) <= horario_atual <= time(20, 0)
        )

        # Ajusta o range de profundidade com base no horário
        if em_horario_pico:
            # Simula mais pessoas: objetos mais próximos do teto (valores mais baixos)
            profundidade_min = 1000  # mm
            profundidade_max = 1800  # mm
        else:
            # Vagão mais vazio
            profundidade_min = 1800
            profundidade_max = 2500

        matriz = np.random.randint(profundidade_min, profundidade_max, size=(self.dim_z, self.dim_y, self.dim_x))

        dados = []
        timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
        for z in range(self.dim_z):
            for y in range(self.dim_y):
                for x in range(self.dim_x):
                    dist = matriz[z, y, x]
                    dados.append([z, y, x, dist, timestamp_str])

        df = pd.DataFrame(dados, columns=["z", "y", "x", "dist_mm", "timestamp"])
        return df

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"/data/{self.sensor_name}/{today}"

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)
