import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sensors.omron_sensor import SensorOmron

if __name__ == "__main__":
    sensor = SensorOmron()
    df = sensor.generate_data()

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "sensor_omron_example.csv")
    df.to_csv(output_path, index=False)

    print(f"Arquivo gerado com sucesso: {output_path}")
    print(df.head())
