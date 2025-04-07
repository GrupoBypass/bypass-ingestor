import os
import random
import pandas as pd

from datetime import datetime, timedelta
from sensors.base_sensor import BaseSensor

class SensorOptical(BaseSensor):
    def __init__(self, qtdGerada):
        super().__init__("Optical")
        self.distancia = 40.0       # mm inicial de acordo com o doc
        self.limite_troca = 9.5     # mm limite de troca de acordo com o doc
        self.qtdGerada = qtdGerada

    def generate_data(self) -> pd.DataFrame:
        dados_simulados = []
        distancia_atual = self.distancia

        for i in range(self.qtdGerada):
            desgaste = random.uniform(0.1, 0.5)
            distancia_atual -= desgaste
            if distancia_atual < 0:
                distancia_atual = 0.0

            dado = self._get_random_data(distancia_atual)
            dados_simulados.append(dado)
        
        df = pd.DataFrame(dados_simulados)
        return df

    def _get_random_data(self, distancia_atual):
        status = "OK" if distancia_atual > self.limite_troca else "TROCAR"
        return {
            "timestamp": datetime.now().isoformat(),
            "distancia_pastilha_mm": round(distancia_atual, 2),
            "status_pastilha": status
        }

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"/data/{self.sensor_name}/{today}"

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)