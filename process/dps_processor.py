import os
from datetime import datetime, timedelta
from sensors.dps_sensor import SensorDPS

class DPSProcessor:
    def __init__(self, qtdGerada: int):
        self.data_inicial = datetime.now() - timedelta(days=1)
        self.qtdGerada = qtdGerada
        self.sensor = SensorDPS(0.10, 42)

    def generate_data_list(self) -> list:
        dados_simulados = []

        for i in range(self.qtdGerada):
            intervalo = 10 + i % 6  # 10 a 15 min (apenas para variar)
            data_hora = self.data_inicial + timedelta(minutes=i * intervalo)
            dado = self.sensor.generate_data()
            dados_simulados.append(dado)

        return dados_simulados
