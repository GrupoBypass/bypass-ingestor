import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.piezo_processor import PiezoProcessor

if __name__ == "__main__":
    processor = PiezoProcessor()
    df = processor.generate_dataframe()

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "sensor_piezo_example.csv")
    df.to_csv(output_path, index=False)

    print(f"Arquivo gerado com sucesso: {output_path}")
    print(df.head())
