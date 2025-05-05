import numpy as np
from datetime import datetime, time
from sensors.base_sensor import BaseSensor

class SensorToF(BaseSensor):
    def __init__(self):
        super().__init__("tof")

        self.comprimento_m = 20.0
        self.largura_m = 2.8
        self.altura_m = 2.5

        self.resolucao_voxel_m = {
            'z': 0.25,
            'y': 0.10,
            'x': 0.20
        }

        self.dim_z = int(self.altura_m / self.resolucao_voxel_m['z'])
        self.dim_y = int(self.largura_m / self.resolucao_voxel_m['y'])
        self.dim_x = int(self.comprimento_m / self.resolucao_voxel_m['x'])

    def generate_raw_matrix(self):
        now = datetime.now()
        horario_atual = now.time()

        em_horario_pico = (
            time(6, 0) <= horario_atual <= time(9, 0) or
            time(17, 0) <= horario_atual <= time(20, 0)
        )

        if em_horario_pico:
            profundidade_min = 1000
            profundidade_max = 1800
        else:
            profundidade_min = 1800
            profundidade_max = 2500

        matriz = np.random.randint(profundidade_min, profundidade_max,
                                   size=(self.dim_z, self.dim_y, self.dim_x))

        return matriz, now  # retorna a matriz bruta e o timestamp
