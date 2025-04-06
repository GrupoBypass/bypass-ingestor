import pandas as pd
import os

class CSVWriter:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    #TODO: Implementar com o lakehouse (realizar conexão) e testar
    # Por enquanto escreve em uma pasta no próprio docker do ingestor
    def write(self, df: pd.DataFrame, relative_path: str):
        # Função write espera o dataframe e o caminho de pasta para os dados do sensor em questão
        full_path = os.path.join(self.base_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        df.to_csv(full_path, index=False)