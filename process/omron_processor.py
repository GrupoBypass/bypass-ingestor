import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.ndimage import gaussian_filter
from sensors.omron_sensor import SensorOmron
from matplotlib.colors import LinearSegmentedColormap


class OmronProcessor:
    def __init__(self, hotspots, percent, noise, radius_min, radius_max, lines, columns):
        self.sensor = SensorOmron(hotspots, percent, noise, radius_min, radius_max, lines, columns)

    def generate_dataframe(self) -> pd.DataFrame:
        matriz = self.sensor.generate_matrix()
        return pd.DataFrame(matriz)
