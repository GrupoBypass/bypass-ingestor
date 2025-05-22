import os
import pandas as pd
from datetime import datetime, timedelta, time
import numpy as np

from sensors.tof_sensor import SensorToF

class ToFProcessor:
    def __init__(self):
        self.sensor = SensorToF()

    def generate_data(self, cenario="BOM", trens=1, carros=6, single_capture=False) -> pd.DataFrame:
        """
        Simula a captura de dados de sensores ToF para diferentes cenários.
        
        Parâmetros:
        - cenario: str ("BOM", "NORMAL", "RUIM") - define o padrão de distribuição das distâncias
        - carros: int - número de carros/carruagens a simular
        - single_capture: bool - se True, gera apenas uma captura no tempo atual
        
        Retorna:
        - DataFrame com colunas ["y", "x", "dist_mm", "timestamp", "trem", "carro"]
        """
        DATA_INICIO = datetime.now()
        start_time = DATA_INICIO.replace(hour=4, minute=30, second=0)
        end_time = start_time.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        current_time = start_time
        
        dados = []
        while current_time < end_time:
            # Definir se estamos em horário de pico
            em_horario_pico = (
                time(6, 0) <= time(current_time.hour) <= time(9, 0) or
                time(17, 0) <= time(current_time.hour) <= time(20, 0)
            )

            # Ajusta o range de profundidade com base no horário
            if em_horario_pico:
                profundidade_min = 1000  # mm
                profundidade_max = 1800  # mm
            else:
                profundidade_min = 1800
                profundidade_max = 2500

            dim_y = 28
            dim_x = 100

            timestamp_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            
            for t in range(1, trens + 1):
                for c in range(1, carros + 1):
                    for y in range(dim_y):
                        for x in range(dim_x):
                            dist = self.generate_dist(cenario, c, profundidade_min, profundidade_max)
                            dados.append([y, x, dist, timestamp_str, t, c])

            if single_capture:
                break
            current_time += timedelta(minutes=3)

        return pd.DataFrame(dados, columns=["y", "x", "dist_mm", "timestamp", "trem", "carro"])
    
    def generate_dist(self, cenario: str, carro: int, profundidade_min: int, profundidade_max: int) -> float:
        # Lógica de geração de distância baseada no cenário
        if cenario == "RUIM":
            if carro == 1:
                dist = np.random.randint(profundidade_min, profundidade_max) * (abs(np.random.random() + 0.01))
            else:
                dist = np.random.randint(profundidade_min, profundidade_max) * (abs(np.random.random() + 0.43))
        elif cenario == "NORMAL":
            if carro == 1 or carro == 6:
                dist = np.random.randint(profundidade_min, profundidade_max) * (abs(np.random.random() + 0.5))
            else:
                dist = np.random.randint(profundidade_min, profundidade_max) * (abs(np.random.random() + 0.25))
        else:  # Cenário "BOM" ou padrão
            dist = np.random.randint(profundidade_min, profundidade_max) * (abs(np.random.random() + 0.41))
        
        # Garante que a distância não ultrapasse o máximo teórico
        if dist > 2500:
            dist = 2500

        return dist

    def aggregate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby(['trem','carro'])
                .apply(lambda x: (x['dist_mm'] < 1800).mean() * 100)
                .reset_index(name='ocupacao')
        )

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"/data/{self.sensor.sensor_name}/{today}"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        path = self.get_output_path()
        df.to_csv(path, index=False)
