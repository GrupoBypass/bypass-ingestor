import random
from datetime import datetime, timedelta
from sensors.base_sensor import BaseSensor
import numpy as np

class SensorPiezo(BaseSensor):
    def __init__(self):
        super().__init__("piezo")
        self.pressure_range = (0.0, 1200.0)  # kPa

    def generate_raw_data(self):
        dados_simulados = []
        now = datetime.now()
        start_time = now.replace(hour=4, minute=30, second=0)
        end_time = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        current_time = start_time

        while current_time < end_time:
            pressure = self._generate_pressure(current_time)
            dados_simulados.append({
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "pressure_kpa": round(pressure, 2)
            })
            current_time += self._get_interval(current_time)

        return dados_simulados

    def _generate_pressure(self, timestamp):
        hour = timestamp.hour

        if (7 <= hour < 9) or (17 <= hour < 19):
            base_pressure = random.uniform(800, 1200)
            return base_pressure * (0.9 + 0.1 * np.sin(timestamp.minute * np.pi / 2.5))
        elif 6 <= hour < 22:
            base_pressure = random.uniform(400, 800)
            return base_pressure * (0.9 + 0.1 * np.sin(timestamp.minute * np.pi / 3))
        else:
            return random.uniform(0, 50)

    def _get_interval(self, timestamp):
        if 6 <= timestamp.hour < 22:
            return timedelta(seconds=random.uniform(45, 120))
        else:
            return timedelta(seconds=random.uniform(120, 300))
