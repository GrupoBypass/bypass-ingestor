import numpy as np
from datetime import datetime
from sensors.base_sensor import BaseSensor

class SensorOptical(BaseSensor):
    def __init__(self, seed, falha_probabilidade: float, limite_troca: float):

        super().__init__("optical")
        self.falha_probabilidade = falha_probabilidade
        self.seed = seed
        self.limite_troca = limite_troca

    def generate_data(self, distancia_atual, data_hora: datetime):
        np.random.seed(self.seed)

        status = np.random.choice(["OK", "ERR"],
                                  p=[1 - self.falha_probabilidade,
                                      self.falha_probabilidade]
                                  )
        
        if status == "OK":
            desgaste = np.random.uniform(0.5, 1.0)
        else:
            desgaste = np.random.uniform(1.5, 2.5)
        
        distancia_atual = max(0.0, distancia_atual - desgaste)

        status = "OK" if distancia_atual > self.limite_troca else "TROCAR"

        return {
            "dataHora": data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "distancia_pastilha_mm": round(distancia_atual, 2),
            "status_pastilha": status
        }, distancia_atual
