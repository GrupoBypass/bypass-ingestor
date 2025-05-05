import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sensors.omron_sensor import SensorOmron

class OmronProcessor:
    def __init__(self, x=50, y=50):
        self.sensor = SensorOmron(x, y)

    def generate_dataframe(self) -> pd.DataFrame:
        matriz = self.sensor.generate_matrix()
        return pd.DataFrame(matriz)

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"data/{self.sensor.sensor_name}/{today}"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)

    def plot_heatmap(self, df: pd.DataFrame):
        plt.imshow(df.values, cmap="Greys", interpolation="nearest")
        plt.title("Matriz Sensor Omron")
        plt.colorbar(label="Valor")
        plt.xlabel("Coluna")
        plt.ylabel("Linha")
        plt.tight_layout()
        # plt.show()
