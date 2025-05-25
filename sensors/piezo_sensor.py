from sensors.base_sensor import BaseSensor
import numpy as np

class SensorPiezo(BaseSensor):
    def __init__(self, seed):
        super().__init__("piezo")
        self.seed = seed

    def generate_data(self, data_hora, base_pressure1, base_pressure2, indice) -> dict:
        np.random.seed(self.seed)

        if(base_pressure1 == None):
            pressure = np.random.uniform(0, 50)
        
        else:
            base_pressure = np.random.uniform(base_pressure1, base_pressure2)
            pressure = base_pressure * (0.9 + 0.1 * np.sin(data_hora.minute * np.pi / indice))

        return {
            "dataHora": data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "pressure_kpa": round(pressure, 2)
        }
