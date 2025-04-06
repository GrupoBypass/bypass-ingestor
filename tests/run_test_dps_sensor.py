import os
import sys
import pandas as pd

# Adiciona a raiz do projeto para importar os sensores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sensors.dps_sensor import SensorDPS

if __name__ == "__main__":
    sensor = SensorDPS()
    df = sensor.generate_data()

    # Caminho local para salvar o exemplo
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "sensor_dps_example.csv")
    df.to_csv(output_path, index=False)

    print(f"Arquivo gerado com sucesso: {output_path}")
    print(df.head())
