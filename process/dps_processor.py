import os
import pandas as pd
from datetime import datetime, timedelta
from sensors.dps_sensor import SensorDPS

class DPSProcessor:
    def __init__(self, qtdGerada: int):
        self.sensor = SensorDPS()
        self.qtdGerada = qtdGerada

    def generate_dataframe(self) -> pd.DataFrame:
        data_inicial = datetime.now() - timedelta(days=1)
        dados_simulados = []

        for i in range(self.qtdGerada):
            intervalo = 10 + i % 6  # 10 a 15 min (apenas para variar)
            data_hora = data_inicial + timedelta(minutes=i * intervalo)
            dado = self.sensor.generate_raw_data(data_hora)
            dados_simulados.append(dado)

        return pd.DataFrame(dados_simulados)

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

# Exemplo de uso:
if __name__ == "__main__":
    processor = DPSProcessor(qtdGerada=100)
    df = processor.generate_dataframe()
    processor.save_data(df)
