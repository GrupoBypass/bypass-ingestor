import os
import pandas as pd
from datetime import datetime, timedelta
from sensors.dps_sensor import SensorDPS

class DPSProcessor:
    def __init__(self, qtdGerada: int):
        self.sensor = SensorDPS()
        self.qtdGerada = qtdGerada

    def generate_dataframe(self) -> str:
        data_inicial = datetime.now() - timedelta(days=1)
        dados_simulados = []

        for i in range(self.qtdGerada):
            intervalo = 10 + i % 6  # 10 a 15 min
            data_hora = data_inicial + timedelta(minutes=i * intervalo)
            dado = self.sensor.generate_raw_data(data_hora)
            dados_simulados.append(dado)

        df = pd.DataFrame(dados_simulados)

        # Converte o DataFrame para um JSON string
        json_str = df.to_json(orient='records', date_format='iso')

        return json_str


    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"./data/dps/{today}"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-dps.csv")

    def save_data(self, df: pd.DataFrame):
        path = self.get_output_path()
        df.to_csv(path, index=False)
        print(f"Arquivo salvo em: {path}")