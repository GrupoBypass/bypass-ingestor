import os
import pandas as pd

# Adiciona a raiz do projeto para conseguir importar os sensores
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sensors.gps_sensor import SensorGPS

if __name__ == "__main__":
    sensor = SensorGPS()
    df = sensor.generate_data()

    # Caminho local para salvar o arquivo
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "sensor_gps_example.csv")
    df.to_csv(output_path, index=False)

    print(f"Arquivo salvo em: {output_path}")
    print(df.head())