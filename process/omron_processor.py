import pandas as pd
from sensors.omron_sensor import SensorOmron
import json

class OmronProcessor:
    def __init__(self, hotspots, percent, noise, radius_min, radius_max, lines, columns):
        self.sensor = SensorOmron(hotspots, percent, noise, radius_min, radius_max, lines, columns, seed=46)

    def generate_data_list(self) -> list:
        matriz = self.sensor.generate_matrix()
        
        json_str = matriz.to_json(orient='records', date_format='iso')
        json_obj = json.loads(json_str)
        
        return json_obj
