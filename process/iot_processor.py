import pandas as pd
import json
from cloud.iot_interface import AzureIoTInterface

class IOTProcessor:
    def __init__(self, df):
        self.df = df

    def insert_azure(self):
        connection_string = "HostName=barbara02231047.azure-devices.net;DeviceId=gabriel-device;SharedAccessKey=dmavQPyvC1JQmqhRcWjbB/ZhiCeBFbWCW0l2HNRTEBU="
        iot_interface = AzureIoTInterface(connection_string=connection_string)
        iot_interface.send_message(self.df)