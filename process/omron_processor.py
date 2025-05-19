import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.ndimage import gaussian_filter
from sensors.omron_sensor import SensorOmron
from matplotlib.colors import LinearSegmentedColormap


class OmronProcessor:
    def __init__(self, hotspots, percent, noise, radius_min, radius_max, lines, columns):
        self.sensor = SensorOmron(hotspots, percent, noise, radius_min, radius_max, lines, columns)

    def generate_dataframe(self) -> pd.DataFrame:
        matriz = self.sensor.generate_matrix()
        return matriz

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"data/{self.sensor.sensor_name}/{today}"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)
