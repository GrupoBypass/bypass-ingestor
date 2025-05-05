import random
from sensors.base_sensor import BaseSensor

class SensorOmron(BaseSensor):
    def __init__(self, x=50, y=50):
        super().__init__("omron")
        self.x = x
        self.y = y

    def generate_matrix(self):
        """Gera uma matriz x por y com valores 0 ou 1"""
        matriz = [[random.randint(0, 1) for _ in range(self.y)] for _ in range(self.x)]
        return matriz
