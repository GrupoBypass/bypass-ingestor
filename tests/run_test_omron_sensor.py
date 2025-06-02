import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.omron_processor import OmronProcessor
from process.iot_processor import IOTProcessor

if __name__ == "__main__":

    processor = OmronProcessor(
        hotspots=0, percent=0.6, noise=0.005,
        radius_min=2, radius_max=4, lines=20, columns=40,
        porta_hotspots=[[10, 20],[20, 30]]  # centro
    )

    # processor = OmronProcessor(
    #     hotspots=0, percent=0.8, noise=0.08,
    #     radius_min=2, radius_max=5, lines=20, columns=40,
    #     porta_hotspots=[[0, 10], [30, 39]]
    # )
    
    # processor = OmronProcessor(
    #     hotspots=3, percent=0.6, noise=0.02,
    #     radius_min=2, radius_max=4, lines=20, columns=40,
    #     porta_hotspots=[]
    # )

    # processor = OmronProcessor(
    #     hotspots=8, percent=0.6, noise=0.2,
    #     radius_min=2, radius_max=4, lines=20, columns=40,
    #     porta_hotspots=[]
    # )
    
    lista = processor.generate_data_list()
        
    save = IOTProcessor(lista)
    save.insert_azure()

    # output_dir = os.path.join(os.path.dirname(__file__), "output")
    # os.makedirs(output_dir, exist_ok=True)

    # output_path = os.path.join(output_dir, "sensor_omron_example.csv")
    # df.to_csv(output_path, index=False)

    # print(f"Arquivo gerado com sucesso: {output_path}")
    # print(df.head())
