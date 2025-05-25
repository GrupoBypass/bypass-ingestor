import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.dht11_processor import DHT11Processor
from process.iot_processor import IOTProcessor

if __name__ == "__main__":
    qtd_dados = 10
    processor = DHT11Processor(qtdGerada=qtd_dados)

    df = processor.generate_data_list()
    print(df)
    
    save = IOTProcessor(df)
    save.insert_azure()

    # output_dir = os.path.join(os.path.dirname(__file__), "output")
    # os.makedirs(output_dir, exist_ok=True)

    # output_path = os.path.join(output_dir, "sensor_dht11_example.csv")
    # df.to_csv(output_path, index=False)

    # print(f"Arquivo gerado com sucesso: {output_path}")
    # print(df.head())
