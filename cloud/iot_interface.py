from azure.iot.device import IoTHubDeviceClient
import json


class AzureIoTInterface:

    def __init__(self, connection_string: str):
        self.device_client = IoTHubDeviceClient.create_from_connection_string(
            connection_string
        )

    def send_message(self, message: dict):
        try:
            message_json = json.dumps(message)

            self.device_client.send_message(message=message_json)

            return True

        except Exception as e:
            print(f"Failed to send message to device: {e}")
            return False
