import os
import sys
import pandas as pd

# Adiciona a raiz do projeto para conseguir importar os sensores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sensors.tof_sensor import SensorToF

if __name__ == "__main__":
    sensor = SensorToF()
    df = sensor.generate_data()

    # Caminho local para salvar o arquivo
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "sensor_tof_example.csv")
    df.to_csv(output_path, index=False)

    print(f"Arquivo salvo em: {output_path}")
    print(df.head())