import random
from datetime import datetime, timedelta

from sensors.piezo_sensor import SensorPiezo

class PiezoProcessor:
    def __init__(self, start_time, end_time):
        self.sensor = SensorPiezo(seed=45)
        self.start_time = start_time
        self.end_time = end_time

    def generate_data_list(self) -> list:
        dados_simulados = []

        current_time = self.start_time

        while current_time < self.end_time:
            hour = current_time.hour

            if (7 <= hour < 9) or (17 <= hour < 19):
                base_pressure1 = 800
                base_pressure2 = 1200
                indice = 2.5

            elif 6 <= hour < 22:
                base_pressure1 = 400
                base_pressure2 = 800
                indice = 3.0

            else:
                base_pressure1 = None
                base_pressure2 = None
                indice = None

            dado = self.sensor.generate_data(current_time,base_pressure1,base_pressure2, indice)
            dados_simulados.append(dado)

            current_time += self._get_intevalo_tempo(current_time)

        return dados_simulados
    
    def _get_intevalo_tempo(self, data_hora: datetime):
        if 6 <= data_hora.hour < 22:
            return timedelta(seconds=random.uniform(45, 120))
        else:
            return timedelta(seconds=random.uniform(120, 300))


