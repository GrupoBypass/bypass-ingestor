import os
import sys
import pandas as pd
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process.dht11_processor import DHT11Processor
from process.iot_processor import IOTProcessor

if __name__ == "__main__":
    qtd_dados = 45 # 1h30 de simulação
    
    # Cenário BOM
    falha_probabilidade = 0.10
    
    # Cenário ALERTA
    # falha_probabilidade = 0.50
    
    # CENÁRIO CRITICO
    # falha_probabilidade = 0.70

    # Estou definindo a data aqui pois, posso querer simular os dados em horário de pico, ai já passo a dt e hr como 12h00
    processor = DHT11Processor(
        qtdGerada=qtd_dados,
        falha_probabilidade= falha_probabilidade,
        data_inicial= datetime.now()
    )
    
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
