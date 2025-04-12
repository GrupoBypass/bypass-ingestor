import os
import random
import pandas as pd
from datetime import datetime, timedelta
from .base_sensor import BaseSensor
import numpy as np

class SensorToF(BaseSensor):
    def __init__(self, grid_shape=(4, 10)):
        super().__init__("tof")
        self.grid_shape = grid_shape  # (linhas, colunas) representando áreas do vagão
        
    def generate_data(self) -> pd.DataFrame:
        dados_simulados = []
        now = datetime.now()
        start_time = now.replace(hour=4, minute=30, second=0)  # Início da operação
        end_time = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)  # Fim do dia
        
        current_time = start_time
        
        while current_time < end_time:
            # Gera matriz volumétrica baseada no horário
            volume_matrix = self._generate_volume_matrix(current_time)
            
            dados_simulados.append({
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "volume_matrix": self._matrix_to_string(volume_matrix),
                "grid_shape": f"{self.grid_shape[0]}x{self.grid_shape[1]}",
                "occupancy_percent": round(np.mean(volume_matrix), 1)  # Ocupação média
            })
            
            # Intervalo aleatório entre 1-5 minutos
            current_time += timedelta(minutes=random.uniform(1, 5))

        return pd.DataFrame(dados_simulados)

    def _generate_volume_matrix(self, timestamp):
        """Gera matriz de ocupação baseada no horário"""
        rows, cols = self.grid_shape
        hour = timestamp.hour
        
        # Define o padrão de ocupação conforme horário
        if (7 <= hour < 9) or (17 <= hour < 19):  # Horário de pico
            base_occupancy = random.uniform(70, 100)
            noise = np.random.normal(0, 10, size=self.grid_shape)
        elif 6 <= hour < 22:  # Horário comercial normal
            base_occupancy = random.uniform(30, 70)
            noise = np.random.normal(0, 15, size=self.grid_shape)
        else:  # Madrugada
            base_occupancy = random.uniform(0, 30)
            noise = np.random.normal(0, 5, size=self.grid_shape)
        
        # Cria gradiente de ocupação (mais cheio perto das portas)
        grad = np.linspace(0.8, 1.2, cols)
        matrix = np.outer(np.ones(rows), grad) * base_occupancy
        
        # Adiciona ruído e limita valores entre 0-100
        matrix = np.clip(matrix + noise, 0, 100)
        
        return np.round(matrix, 1)

    def _matrix_to_string(self, matrix):
        """Converte a matriz numpy para string formatada"""
        return "[" + "|".join([
            "[" + ",".join([f"{val:.1f}" for val in row]) + "]"
            for row in matrix
        ]) + "]"

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"data/{self.sensor_name}/{today}"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)