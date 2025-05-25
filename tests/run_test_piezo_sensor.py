import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.piezo_processor import PiezoProcessor
from process.iot_processor import IOTProcessor

if __name__ == "__main__":
    
    # Dentro do processor, já existe um clculo que simula os dados em horário de pico,por isso não é passado porcentagem de falha

    now = datetime.now()
    start_time = now.replace(hour=4, minute=30, second=0)
    end_time = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)

    # Dados de 1 dia (4h30 até 23h59)
    processor = PiezoProcessor(start_time=start_time, end_time=end_time)
    df = processor.generate_data_list()

    print(df)

    save = IOTProcessor(df)
    save.insert_azure()

    # output_dir = os.path.join(os.path.dirname(__file__), "output")
    # os.makedirs(output_dir, exist_ok=True)

    # output_path = os.path.join(output_dir, "sensor_piezo_example.csv")
    # df.to_csv(output_path, index=False)

    # print(f"Arquivo gerado com sucesso: {output_path}")
    # print(df.head())
