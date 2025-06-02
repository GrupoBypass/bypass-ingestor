from sensors.omron_sensor import SensorOmron

class OmronProcessor:
    def __init__(self, hotspots, percent, noise,radius_min, radius_max, lines, columns, porta_hotspots):
        self.sensor = SensorOmron(hotspots, percent, noise,radius_min, radius_max, lines, columns, porta_hotspots)

    def generate_data_list(self) -> list:
        lista = self.sensor.generate_matrix()
        return lista