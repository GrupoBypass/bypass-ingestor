import pandas as pd
from datetime import datetime, timedelta
from sensors.optical_sensor import SensorOptical

class OpticalProcessor:
    def __init__(self, qtdGerada, falha_probabilidade, distancia_inicial, distancia_final):
        self.sensor = SensorOptical(falha_probabilidade=falha_probabilidade, seed=44, limite_troca= distancia_final)
        self.data_inicial = datetime.now() - timedelta(days=1)
        self.qtdGerada = qtdGerada
        self.distancia_inicial = distancia_inicial

    def generate_data_list(self) -> list:
        dados_simulados = []
        distancia_inicial = self.distancia_inicial
        
        for i in range(self.qtdGerada):
            data_hora = self.data_inicial + timedelta(days=i)

            dado = self.sensor.generate_data(distancia_inicial, data_hora)
            distancia_inicial = dado[1]
            
            dados_simulados.append(dado[0])

        return dados_simulados
