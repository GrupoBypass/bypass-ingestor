import os
import pandas as pd

from sensors.tof_sensor import SensorToF

from datetime import time, datetime, timedelta
import numpy as np
import random

class ToFProcessor:
    def __init__(self):
        self.sensor = SensorToF()

    def generate_dataframe(self, sensor_id: int, single_capture:bool=False, horario: str="") -> pd.DataFrame:
        """
        Simula a captura de dados de sensores ToF para diferentes cenários.
        
        Parâmetros:
        - sensor_id: int
        - single_capture: bool - se True, gera apenas uma captura no tempo atual
        - horario: str - "HH:MM", se vazio pega o horário atual
        
        Retorna:
        - DataFrame com colunas ["y", "x", "dist_mm", "timestamp", "sensor_id"]
        """
        
        car_dimensions = {
            'comprimento': 20,
            'largura': 2.8,
            'altura': 2.5
        }

        DATA_INICIO = datetime.now()

        LIMIAR_OCUPACAO = 1800  # Distância abaixo disso considera ocupado
        DIST_MAXIMA = 2500      # Distância máxima esperada

        LAYOUTS = {
        "stairs_ends": {
            "name": "stairs_ends",
            "wagon_crowding": {
                "wagons_affected": (1, 6),
                "multiplier": (0.85, 0.95)
            },
            "door_effect": {
                "base_value": -350,
                "noise": 0.05
            },
            "noise": 0.1
        },
        "central_stairs": {
            "name": "central_stairs",
            "wagon_crowding": {
                "wagons_affected": (3, 4),
                "multiplier": (0.85, 0.95)  # Stronger effect for middle wagons
            },
            "door_effect": {
                "base_value": -250,
                "noise": 0.05
            },
            "noise": 0.1
        },
        "balanced": {
            "name": "balanced",
            "wagon_crowding": {
                "wagons_affected": (1, 2, 3, 4, 5, 6),
                "multiplier": (0.9, 1.05)
            },
            "door_effect": {
                "base_value": -250,
                "noise": 0.1
            },
            "noise": 0.15
        },
    }

        start_time = DATA_INICIO.replace(hour=4, minute=30, second=0)
        end_time = start_time.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        
        if horario == "":
            current_time = start_time
        else:
            str_horas, str_min = horario.split(":")
            current_time = start_time.replace(hour=int(str_horas), minute=int(str_min), second=0)
            
        dados = []
        while current_time < end_time:
            dim_y = 28
            dim_x = 100

            timestamp_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            print(timestamp_str)

            layout = random.choice(list(LAYOUTS.values()))
            print("layout ", layout["name"])
            
            c = random.randint(1,6)

            for y in range(dim_y):
                for x in range(dim_x):
                    dist = self.generate_dist(c, x, y, timestamp_str, layout)
                    dados.append([y, x, dist, timestamp_str, sensor_id])

            if single_capture:
                break
            current_time += timedelta(minutes=3)

        return pd.DataFrame(dados, columns=["y", "x", "dist_mm", "timestamp", "sensor_id"])
    
    def generate_dist(self, carro: int, x: int, y: int, timestamp: str, layout: dict, ) -> float:
        """
        Generates distance values where:
        - Lower values = more crowded (object close to sensor)
        - Higher values (≈2500) = empty space (floor visible)
        
        Args:
            x, y: Coordinates (0-99, 0-27)
            carro: Wagon number (1-6)
            cenario: Scenario ("BOM", "NORMAL", "RUIM")
        
        Returns:
            Distance in mm (1000-2500, where 1000=max crowding)
        """
        
        base_dist = 2000
        
        # Parse timestamp (assuming format "YYYY-MM-DD HH:MM:SS")
        current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        
        # time_mult = get_time_factor(current_time)
        time_mult = self.get_wagon_time_factor(current_time, carro, layout)
        
        # Door effect
        door_positions = [12, 37, 62, 87]
        door_effect = 0
        
        nearest_door_dist = min(abs(x - door) for door in door_positions)
        if nearest_door_dist <= 4:
            door_effect += layout["door_effect"]["base_value"]
            door_effect *= random.uniform(1 - layout["door_effect"]["noise"], 1 + layout["door_effect"]["noise"])
                
        # Wagon multiplier
        base_mult = 1
        if carro in layout["wagon_crowding"]["wagons_affected"]:
            base_mult = random.uniform(*layout["wagon_crowding"]["multiplier"])
        
        final_dist = (base_dist + door_effect) * base_mult * time_mult
        
        # Apply effects
        final_dist *= random.uniform(1 - layout["noise"], 1 + layout["noise"])
        
        return np.clip(final_dist, 1000, 2500)
    
    def get_time_factor(current_time: datetime) -> float:
        """
        Returns time-based crowding multiplier (0.8-1.0) where:
        - Lower values = more crowded
        - Smooth transitions between periods
        """
        minutes = current_time.hour * 60 + current_time.minute
        
        # Morning ramp-up (4:30-7:00)
        if 270 <= minutes < 420:  # 4:30-7:00
            # Linear from 1.0 → 0.95
            return 1.0 - (minutes - 270) / (420 - 270) * 0.05
        
        # Morning peak (7:00-9:00)
        elif 420 <= minutes < 540:  # 7:00-9:00
            return 0.95  # Peak crowding
        
        # Morning cool-down (9:00-10:30)
        elif 540 <= minutes < 630:  # 9:00-10:30
            # Linear from 0.95 → 1.0
            return 0.95 + (minutes - 540) / (630 - 540) * 0.05
        
        # Evening ramp-up (16:00-18:00)
        elif 960 <= minutes < 1080:  # 16:00-18:00
            # Linear from 1.0 → 0.95
            return 1.0 - (minutes - 960) / (1080 - 960) * 0.05
        
        # Evening peak (18:00-20:00)
        elif 1080 <= minutes < 1200:  # 18:00-20:00
            return 0.95  # Peak crowding
        
        # Evening cool-down (20:00-22:00)
        elif 1200 <= minutes < 1320:  # 20:00-22:00
            # Linear from 0.95 → 1.0
            return 0.95 + (minutes - 1200) / (1320 - 1200) * 0.05
        
        # Off-peak (all other times)
        return 1.0

    def get_wagon_time_factor(self, current_time: datetime, carro: int, layout: dict) -> float:
        """
        Returns time multiplier with:
        - Stronger time effects for non-layout wagons (0.7-1.1)
        - Weaker time effects for layout-affected wagons (0.85-1.05)
        """
        base_factor = self.get_time_factor(current_time)  # From previous implementation
        
        # Check if wagon is affected by layout
        is_layout_wagon = (
            carro in layout.get("wagon_crowding", {}).get("wagons_affected", [])
        )
        
        # Apply stronger time effects to non-layout wagons
        if not is_layout_wagon or layout["name"] == "balanced":
            return np.clip(base_factor * 0.9 * random.uniform(0.95, 1.05), 0.85, 0.9)  # Amplified time effect
        return base_factor

    def get_output_path(self):
        today = datetime.today().strftime('%Y-%m-%d')
        output_dir = f"/data/{self.sensor.sensor_name}/{today}"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%H-%M-%S')
        return os.path.join(output_dir, f"{timestamp}-{self.sensor.sensor_name}.csv")

    def save_data(self, df: pd.DataFrame):
        path = self.get_output_path()
        df.to_csv(path, index=False)
