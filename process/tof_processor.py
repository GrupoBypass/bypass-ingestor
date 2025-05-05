import os
import pandas as pd
from datetime import datetime

from sensors.tof_sensor import SensorToF

class ToFProcessor:
    def __init__(self):
        self.sensor = SensorToF()

    def generate_dataframe(self) -> pd.DataFrame:
        matriz, timestamp = self.sensor.generate_raw_matrix()
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        dados = []
        for z in range(self.sensor.dim_z):
            for y in range(self.sensor.dim_y):
                for x in range(self.sensor.dim_x):
                    dist = matriz[z, y, x]
                    dados.append([z, y, x, dist, timestamp_str])

        df = pd.DataFrame(dados, columns=["z", "y", "x", "dist_mm", "timestamp"])
        return df

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"/data/{self.sensor.sensor_name}/{today}"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        path = self.get_output_path()
        df.to_csv(path, index=False)
