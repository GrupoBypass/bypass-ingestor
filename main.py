import logging

from sensors.sensor_gps import SensorGPS
from data_writer.csv_writer import CSVWriter
from utils.file_manager import FileManager
from config import settings

def main():
    sensors = [SensorGPS()]  # adicionar os sensores aqui conforme for desenvolvendo
    writer = CSVWriter(settings.BASE_OUTPUT_DIR)
    FileManager.create_sensor_dirs(settings.BASE_OUTPUT_DIR, settings.SENSOR_LIST)

    for sensor in sensors:
        data = sensor.generate_data()
        output_path = sensor.get_output_path()
        writer.write(data, output_path)

    logging.info("Ingestão de dados efetuados com sucesso no LakeHouse!")
if __name__ == "__main__":
    main()