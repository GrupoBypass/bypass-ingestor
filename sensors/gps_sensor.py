import os
import random
import pandas as pd

from datetime import datetime

from sensors.base_sensor import BaseSensor
from process.distance import calculate_distance

class SensorGPS(BaseSensor):
    def __init__(self):
        super().__init__("gps")

    def generate_data(self) -> pd.DataFrame:
        positions = []
        distances = []

        last_position = self._get_random_position()

        for _ in range(10):  # Gerar 10 pontos
            new_position = self._get_random_position()
            distance = self.calculate_distance(last_position, new_position)
            positions.append(new_position)
            distances.append(distance)
            last_position = new_position

        df = pd.DataFrame(positions, columns=["x", "y", "z"])
        df["distance"] = distances
        return df

    def _get_random_position(self):
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        z = random.randint(-100, 100)
        return (x, y, z)

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"/data/{self.sensor_name}/{today}"

        # Verificar se o diretório existe, senão criar
        os.makedirs(output_dir, exist_ok=True)

        #TODO: deixar o nome do arquivo de acordo com a especificação
        # o código por enquanto está escrevendo assim: 22-34-00-gps (HH-mm-ss)
        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)