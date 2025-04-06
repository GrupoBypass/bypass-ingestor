import os
import pandas as pd
from sensors.gps_sensor import SensorGPS

def test_gps_sensor_generates_file():
    sensor = SensorGPS()
    df = sensor.generate_data()
    
    # Aqui vai escrever em um caminho test no docker, 
    # pode alterar para salvar na sua máquina local.
    test_output_dir = "tests/output"
    os.makedirs(test_output_dir, exist_ok=True) # Comenta isso aqui na hora de testar local!!!!!!!!
    output_path = os.path.join(test_output_dir, "sensor_gps_test.csv")
    
    df.to_csv(output_path, index=False)

    assert os.path.exists(output_path), "O arquivo CSV não foi gerado!"
    
    test_df = pd.read_csv(output_path)
    assert not test_df.empty, "O arquivo CSV está vazio!"

    expected_columns = {"x", "y", "z", "distance"}
    assert expected_columns.issubset(set(test_df.columns)), "Colunas inesperadas no CSV"