import numpy as np
from datetime import datetime, timedelta
from sensors.base_sensor import BaseSensor

class SensorDHT11(BaseSensor):
    def __init__(self, seed):
        super().__init__("dht11")
        self.seed = seed

    # Se ao invés de trabalharmos com horarrio de pico formos usar probabilidade de erro só descomentar construtor abaixo
    
    # def __init__(self, seed, falha_probabilidade: float):
        # super().__init__("dht11")
        # self.falha_probabilidade = falha_probabilidade
        # self.seed = seed
        
    def generate_data(self, dataHora: datetime) -> dict:
        np.random.seed(self.seed)

        # DESCOMENTAR CASO USAR PROBABILIDADE 
        # nivel = np.random.choice(["OK", "ERR"],
        #                           p=[1 - self.falha_probabilidade,
        #                               self.falha_probabilidade]
        #                           )
        # if nivel == "OK":
        #     temp_base = 20.0
        #     umid_base= 45.0
        # else:
        #     temp_base = 30.0
        #     umid_base = 55.0

        hora = dataHora.hour

        if 12 <= hora <= 15:
            temp_base = 30.0
            umid_base = 55.0
        else:
            temp_base = 20.0
            umid_base= 45.0

        temperatura = temp_base + np.random.uniform(-2.0, 2.0)
        umidade = umid_base + np.random.uniform(-5.0, 5.0)

        return {
            "dataHora": dataHora.strftime("%Y-%m-%d %H:%M:%S"),
            "temperatura_c": round(temperatura, 1),
            "umidade_porcentagem": round(umidade, 1)
        }
