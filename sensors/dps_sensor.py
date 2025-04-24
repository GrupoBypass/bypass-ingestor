import random
from datetime import datetime
from sensors.base_sensor import BaseSensor

class SensorDPS(BaseSensor):
    def __init__(self):
        super().__init__("dps")

    def generate_raw_data(self, data_hora_base: datetime) -> dict:
        status = "OK" if random.random() < 0.90 else "FALHA"

        if status == "OK":
            pico_tensao_kv = 0.0
            corrente_surto_ka = 0.0
        else:
            pico_tensao_kv = round(random.uniform(1.0, 12.0), 2)
            corrente_surto_ka = round(random.uniform(5.0, 50.0), 2)

        return {
            "dataHora": data_hora_base.strftime("%Y-%m-%d %H:%M:%S"),
            "statusDPS": status,
            "picoTensao_kV": pico_tensao_kv,
            "correnteSurto_kA": corrente_surto_ka,
        }
