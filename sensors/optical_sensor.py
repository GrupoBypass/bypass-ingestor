import random
from datetime import datetime
from sensors.base_sensor import BaseSensor

class SensorOptical(BaseSensor):
    def __init__(self, qtdGerada=1):
        super().__init__("optical")
        self.distancia = 40.0       # mm inicial
        self.limite_troca = 9.5     # mm limite
        self.qtdGerada = qtdGerada

    def generate_raw_data(self):
        dados_simulados = []
        distancia_atual = self.distancia

        for _ in range(self.qtdGerada):
            desgaste = random.uniform(0.1, 0.5)
            distancia_atual = max(0.0, distancia_atual - desgaste)

            dados_simulados.append(self._get_random_data(distancia_atual))

        return dados_simulados

    def _get_random_data(self, distancia_atual):
        status = "OK" if distancia_atual > self.limite_troca else "TROCAR"
        return {
            "timestamp": datetime.now().isoformat(),
            "distancia_pastilha_mm": round(distancia_atual, 2),
            "status_pastilha": status
        }
