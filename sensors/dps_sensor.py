import numpy as np
from datetime import datetime
from sensors.base_sensor import BaseSensor
import pandas as pd
from datetime import datetime, timedelta


class SensorDPS(BaseSensor):
    def __init__(self, seed, falha_probabilidade: float):
        super().__init__("dps")
        self.falha_probabilidade = falha_probabilidade
        self.seed = seed

    def generate_data(self, data_hora: datetime) -> dict:
        np.random.seed(self.seed)

        status = np.random.choice(["OK", "TROCAR"],
                                  p=[1 - self.falha_probabilidade,
                                      self.falha_probabilidade]
                                  )

        if status == "OK":
            pico_tensao_kv = 0.0
            corrente_surto_ka = 0.0
        else:
            pico_tensao_kv = np.round(np.random.uniform(0.5, 10.0), 2)
            corrente_surto_ka = np.round(np.random.uniform(0.1, 15.0), 2)

        return {
            "dataHora": data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "statusDPS": status,
            "picoTensao_kV": pico_tensao_kv,
            "correnteSurto_kA": corrente_surto_ka,
        }
