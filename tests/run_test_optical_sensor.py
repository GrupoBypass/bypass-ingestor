import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.optical_processor import OpticalProcessor
from process.iot_processor import IOTProcessor

if __name__ == "__main__":
    qtd_dados = 30 # Um mês

    # Cenário BOM
    falha_probabilidade = 0.10

    # Cenário ALERTA
    # falha_probabilidade = 0.40

    # Cenário CRITICO
    # falha_probabilidade = 0.60

    processor = OpticalProcessor(
        qtdGerada= qtd_dados, 
        falha_probabilidade= falha_probabilidade,
        distancia_inicial= 45.0,
        distancia_final= 9.5,
        )
    
    df = processor.generate_data_list()

    print(df)

    save = IOTProcessor(df)
    save.insert_azure()

    # output_dir = os.path.join(os.path.dirname(__file__), "output")
    # os.makedirs(output_dir, exist_ok=True)

    # output_path = os.path.join(output_dir, "sensor_optical_example.csv")
    # df.to_csv(output_path, index=False)

    # print(f"Arquivo gerado com sucesso: {output_path}")
    # print(df.head())
