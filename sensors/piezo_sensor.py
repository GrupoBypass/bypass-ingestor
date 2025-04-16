import os
import random
import pandas as pd
from datetime import datetime, timedelta
from .base_sensor import BaseSensor
import numpy as np

class SensorPiezo(BaseSensor):
    def __init__(self):
        super().__init__("piezo")
        self.pressure_range = (0.0, 1200.0)  # kPa (valores típicos para trilhos)
        
    def generate_data(self) -> pd.DataFrame:
        dados_simulados = []
        now = datetime.now()
        start_time = now.replace(hour=4, minute=30, second=0)  # Início operação
        end_time = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)  # Fim do dia
        
        current_time = start_time
        
        while current_time < end_time:
            # Gera um padrão de pressão baseado no horário
            pressure = self._generate_pressure(current_time)
            dados_simulados.append({
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "pressure_kpa": pressure
            })
            
            # Intervalo entre medições varia conforme horário
            current_time += self._get_interval(current_time)

        return pd.DataFrame(dados_simulados)

    def _generate_pressure(self, timestamp):
        """Gera valores de pressão realistas baseados no horário"""
        hour = timestamp.hour
        
        # Horário de pico (maior pressão)
        if (7 <= hour < 9) or (17 <= hour < 19):
            base_pressure = random.uniform(800, 1200)
            # Adiciona variação senoidal simulando passagem de trens
            return base_pressure * (0.9 + 0.1 * np.sin(timestamp.minute * np.pi / 2.5))
        
        # Horário comercial normal
        elif 6 <= hour < 22:
            base_pressure = random.uniform(400, 800)
            return base_pressure * (0.9 + 0.1 * np.sin(timestamp.minute * np.pi / 3))
        
        # Madrugada (pressão residual)
        else:
            return random.uniform(0, 50)  # Pressão mínima

    def _get_interval(self, timestamp):
        """Define intervalos entre medições conforme horário"""
        if 6 <= timestamp.hour < 22:  # Horário comercial
            return timedelta(seconds=random.uniform(45, 120))  # 45s-2min
        else:  # Madrugada
            return timedelta(seconds=random.uniform(120, 300))  # 2-5min

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"data/{self.sensor_name}/{today}"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)