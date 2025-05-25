import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.omron_processor import OmronProcessor
from process.iot_processor import IOTProcessor

if __name__ == "__main__":
    # Cenário BOM
    processor = OmronProcessor(hotspots=2, percent=0.6, noise=0.005, radius_min=1, radius_max=2, lines=20, columns=30)

    # Cenário ALERTA
    # processor = OmronProcessor(hotspots=5, percent=0.7, noise=0.02, radius_min=1, radius_max=3, lines=20, columns=30)

    # Cenário CRITICO
    # processor = OmronProcessor(hotspots=8, percent=0.9, noise=0.08, radius_min=2, radius_max=4, lines=20, columns=30)

    df = processor.generate_data_list()
    print(df)

    save = IOTProcessor(df)
    save.insert_azure()

    # output_dir = os.path.join(os.path.dirname(__file__), "output")
    # os.makedirs(output_dir, exist_ok=True)

    # output_path = os.path.join(output_dir, "sensor_omron_example.csv")
    # df.to_csv(output_path, index=False)

    # print(f"Arquivo gerado com sucesso: {output_path}")
    # print(df.head())
