import os

SENSOR_LIST = [
    "sensor_gps",
]

#TODO: alterar para caminho base no lakehouse
BASE_OUTPUT_DIR = os.getenv("BASE_OUTPUT_DIR", "/app/data/")

# aqui podemos ir setando a quantidade de samples que queremos gerar para cada sensor
DEFAULT_SAMPLE_SIZE = int(os.getenv("DEFAULT_SAMPLE_SIZE", "10"))

# Configs do lakehouse
DB_CONFIG = {
    "user": os.getenv("DB_USER", "bypass"),
    "password": os.getenv("DB_PASS", "bypass123"),
    "host": os.getenv("DB_HOST", "mysql"),
    "database": os.getenv("DB_NAME", "bypass"),
}