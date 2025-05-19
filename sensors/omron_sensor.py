import random
import numpy as np
import pandas as pd
from sensors.base_sensor import BaseSensor

class SensorOmron(BaseSensor):
    def __init__(self, hotspots, percent, noise, radius_min, radius_max, lines, columns):
        super().__init__("omron")
        self.lines = lines
        self.columns = columns
        self.hotspots = hotspots
        self.percent = percent
        self.noise = noise
        self.radius_min = radius_min 
        self.radius_max = radius_max 

    def generate_matrix(self):
        matriz = np.zeros((self.lines, self.columns))

        for _ in range(self.hotspots):
            centro_x = random.randint(3, self.lines - 4)
            centro_y = random.randint(3, self.columns - 4)
            raio = random.randint(self.radius_min, self.radius_max)

            for i in range(centro_x - raio, centro_x + raio + 1):
                for j in range(centro_y - raio, centro_y + raio + 1):
                    if 0 <= i < self.lines and 0 <= j < self.columns:
                        if random.random() < self.percent:
                            matriz[i][j] = 1

        for i in range(self.lines):
            for j in range(self.columns):
                if matriz[i][j] == 0 and random.random() < self.noise:
                    matriz[i][j] = 1

        porcentagem_ativos = np.sum(matriz) / matriz.size
        # print(f"Porcentagem de áreas ativas: {porcentagem_ativos:.2%}")

        # Conversão para DataFrame com colunas x1, x2... e índice y1, y2...
        df = pd.DataFrame(
            matriz,
            columns=[f"x{i+1}" for i in range(self.columns)],
            index=[f"y{j+1}" for j in range(self.lines)]
        )
        
        return df
