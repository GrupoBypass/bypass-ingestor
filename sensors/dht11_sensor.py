import numpy as np
from datetime import datetime
from sensors.base_sensor import BaseSensor

class SensorDHT11(BaseSensor):
    
    def __init__(self, seed: int, falha_probabilidade: float):
        super().__init__("dht11")
        self.falha_probabilidade = falha_probabilidade
        self.seed = seed
        
    def generate_data(self, dataHora: datetime) -> dict:
        np.random.seed(self.seed)

        nivel = np.random.choice(["OK", "ERR"],
                                  p=[1 - self.falha_probabilidade,
                                      self.falha_probabilidade]
                                  )
        
        if nivel == "OK":
            temperatura = np.random.uniform(17.0, 22.0)
            umidade= np.random.uniform(50.0, 55.0)
        else:
            temperatura = np.random.uniform(27.0, 31.0)
            umidade = np.random.uniform(45.0, 50.0)

        return {
            "dataHora": dataHora.strftime("%Y-%m-%d %H:%M:%S"),
            "temperatura_c": round(temperatura, 2),
            "umidade_porcentagem": round(umidade, 2)
        }
