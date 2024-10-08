import adafruit_connection_manager
from adafruit_matrixportal import network


class RobsNetwork(network.Network):

    @property
    def esp(self):
        return self._wifi.esp

    def add_network(self, ssid, password):

        if not self._wifi_credentials:
            self._wifi_credentials = []

        self._wifi_credentials.append(
            {
                "ssid": ssid,
                "password": password,
            }
        )

    def create_ap(self, ssid, password):
        try:
            if hasattr(self._wifi, "esp"):
                self._wifi.esp.create_AP(ssid, password)
            else:
                self._wifi.start_ap(ssid, password)
            return True
        except:
            print("Could not create AP")
            return False

    def get_socket_pool(self):
        return adafruit_connection_manager.get_radio_socketpool(self._wifi.esp)

    def reset_wifi(self):
        try:
            self.esp.reset()
            self.connect()
            return True
        except Exception as e:
            print(f"Error resetting wifi: {e}")
            return False
