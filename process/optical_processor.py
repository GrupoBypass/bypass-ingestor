import os
import pandas as pd
from datetime import datetime
from sensors.optical_sensor import SensorOptical

class OpticalProcessor:
    def __init__(self, qtdGerada=10):
        self.sensor = SensorOptical(qtdGerada)

    def generate_dataframe(self) -> pd.DataFrame:
        dados = self.sensor.generate_raw_data()
        return pd.DataFrame(dados)

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"data/{self.sensor.sensor_name}/{today}"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)
