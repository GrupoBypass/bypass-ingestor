import os
import pandas as pd
from datetime import datetime
from datetime import datetime, timedelta
import random

from sensors.dht11_sensor import SensorDHT11

class DHT11Processor:
    def __init__(self, qtdGerada: int, falha_probabilidade: float, data_inicial: datetime):
        self.data_inicial = data_inicial
        self.qtdGerada = qtdGerada
        self.sensor = SensorDHT11(seed=43, falha_probabilidade=falha_probabilidade)

    def generate_data_list(self) -> list:
        dados_simulados = []

        for i in range(self.qtdGerada):
            dataHora = (
                self.data_inicial + timedelta(minutes=sum(random.randint(2, 5) for _ in range(i)))
                if i > 0 else self.data_inicial
            )
            dado = self.sensor.generate_data(dataHora)
            dados_simulados.append(dado)

        return dados_simulados
