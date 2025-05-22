import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.tof_processor import ToFProcessor
from process.iot_processor import IOTProcessor

if __name__ == "__main__":
    processor = ToFProcessor()
    df = processor.aggregate_data(processor.generate_data(carros=6, single_capture=True))
    
    save = IOTProcessor(df)
    save.insert_azure()

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "sensor_tof_example.csv")
    df.to_csv(output_path, index=False)

    print(f"Arquivo gerado com sucesso: {output_path}")
    print(df.head())
