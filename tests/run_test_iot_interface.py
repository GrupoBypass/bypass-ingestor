import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud.iot_interface import AzureIoTInterface


def generate_data():
    return {
        "dataHora": "2023-10-01 13:05:00",
        "statusDPS": "FALHA",
        "picoTensao_kV": 5.0,
        "correnteSurto_kA": 10.0
    }


if __name__ == "__main__":
    # connection_string = "HostName=barbara02231047.azure-devices.net;DeviceId=barbara-02231047;SharedAccessKey=pnlb6SNJAah/pOQ7Nq27tmqmhzzB5dclRaqbBRof1pY="
    connection_string = "HostName=barbara02231047.azure-devices.net;DeviceId=gabriel-device;SharedAccessKey=dmavQPyvC1JQmqhRcWjbB/ZhiCeBFbWCW0l2HNRTEBU="

    iot_interface = AzureIoTInterface(connection_string=connection_string)

    data = generate_data()
    print(data)

    iot_interface.send_message(data)
