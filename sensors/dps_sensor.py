import os
import random
import pandas as pd

from datetime import datetime, timedelta
from sensors.base_sensor import BaseSensor

class SensorDPS(BaseSensor):
    def __init__(self, qtdGerada):
        super().__init__("dps")
        self.qtdGerada = qtdGerada

    def generate_data(self) -> pd.DataFrame:
        dados_simulados = []
        data_inicial = datetime.now() - timedelta(days=1)

        for i in range(self.qtdGerada):
            intervalo = random.randint(10, 15)  # Intervalo de 10 a 15 minutos
            data_hora = data_inicial + timedelta(minutes=i * intervalo)
            
            dado = self._get_random_data(data_hora)
            dados_simulados.append(dado)
        
        df = pd.DataFrame(dados_simulados)
        return df

    def _get_random_data(self, data_hora_base):
        status = "OK" if random.random() < 0.90 else "FALHA"
    
        if status == "OK":
            pico_tensao_kv = 0.0
            corrente_surto_ka = 0.0
        else:
            # 1.0 kV a 12.0 kV
            pico_tensao_kv = round(random.uniform(1.0, 12.0), 2)
            
            # 5.0 kA a 50.0 kA
            corrente_surto_ka = round(random.uniform(5.0, 50.0), 2)
        
        return {
            "dataHora": data_hora_base.strftime("%Y-%m-%d %H:%M:%S"),
            "statusDPS": status,
            "picoTensao_kV": pico_tensao_kv,
            "correnteSurto_kA": corrente_surto_ka,
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