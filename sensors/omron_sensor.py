import random
import numpy as np
import pandas as pd
from sensors.base_sensor import BaseSensor

class SensorOmron(BaseSensor):

    def __init__(self, hotspots, percent, noise, radius_min, radius_max, lines, columns, porta_hotspots):
        super().__init__("omron")
        self.hotspots = hotspots
        self.percent = percent
        self.noise = noise
        self.radius_min = radius_min
        self.radius_max = radius_max
        self.lines = lines
        self.columns = columns
        self.porta_hotspots = porta_hotspots or []

    def apply_hotspot(self, matriz, centro_x, centro_y, raio, intensidade_min=0.7, intensidade_max=1.0):
        max_dist = np.sqrt(2) * raio

        for i in range(centro_x - raio, centro_x + raio + 1):
            for j in range(centro_y - raio, centro_y + raio + 1):
                if 0 <= i < self.lines and 0 <= j < self.columns:
                    dist = np.sqrt((centro_x - i) ** 2 + (centro_y - j) ** 2)
                    if dist <= raio:
                        intensidade = max(0, 1 - dist / max_dist)
                        intensidade *= random.uniform(intensidade_min, intensidade_max)
                        matriz[i][j] = max(matriz[i][j], intensidade)


    def generate_matrix(self):
        matriz = np.random.uniform(low=0.0, high=0.1, size=(20, 40))

        # Hotspots normais
        for _ in range(self.hotspots):
            centro_x = random.randint(3, self.lines - 4)
            centro_y = random.randint(3, self.columns - 4)
            raio = random.randint(self.radius_min, self.radius_max)
            self.apply_hotspot(matriz, centro_x, centro_y, raio)

        # Hotspots nas portas
        for inicio, fim in self.porta_hotspots:
            centro_y = (inicio + fim) // 2
            raio = random.randint(self.radius_max, self.radius_max + 2)

            # Porta superior
            centro_x_sup = random.randint(0, 2)
            self.apply_hotspot(matriz, centro_x_sup, centro_y, raio, 0.8, 1.0)

            # Porta inferior
            centro_x_inf = random.randint(self.lines - 3, self.lines - 1)
            self.apply_hotspot(matriz, centro_x_inf, centro_y, raio, 0.8, 1.0)

        # Ruído fraco fora das zonas de aglomeração
        for i in range(self.lines):
            for j in range(self.columns):
                if matriz[i][j] == 0 and random.random() < self.noise:
                    matriz[i][j] = random.uniform(0.05, 0.2)

        lista = []
        for i in range(self.columns):
            for j in range(self.lines):
                valueNow = {
                    "y":j,
                    "x":i,
                    "valor-matriz":matriz[j][i]
                }
                lista.append(valueNow)


        return lista

