import os
import random
import pandas as pd
from datetime import datetime, timedelta
from .base_sensor import BaseSensor  # herda a estrutura base

import random
from datetime import datetime, timedelta
from sensors.base_sensor import BaseSensor

class SensorDHT11(BaseSensor):
    def __init__(self):
        super().__init__("dht11")

        self.temp_range = (20.0, 40.0)
        self.humidity_range = (30.0, 70.0)

    def generate_raw_data(self):
        dados_simulados = []
        data_inicial = datetime.now()

        for i in range(108):
            timestamp = (
                data_inicial + timedelta(minutes=sum(random.randint(2, 5) for _ in range(i)))
                if i > 0 else data_inicial
            )
            dado = self._get_random_data(timestamp)
            dados_simulados.append(dado)

        return dados_simulados

    def _get_random_data(self, timestamp):
        hora = timestamp.hour
        if 6 <= hora <= 9 or 17 <= hora <= 20:
            passageiros = random.randint(150, 200)
        else:
            passageiros = random.randint(30, 100)

        base_temp = 22
        temperatura = base_temp + (passageiros * 0.04) + random.uniform(-1, 1)

        base_umidade = 45
        umidade = base_umidade + (passageiros * 0.05) + random.uniform(-2, 2)

        return {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature_c": round(temperatura, 1),
            "humidity_percent": round(umidade, 1)
        }
