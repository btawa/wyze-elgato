import sys
import threading
import os
from wyze_sdk import Client
from decouple import Config, RepositoryEnv
from wyze_sdk.errors import WyzeApiError


class WyzeController:
    def __init__(self, user, password, bulb_list):
        try:
            self.client = Client(email=user, password=password)
        except Exception as e:
            sys.exit(f"Client cannot connect to API: {e}")

        self.bulbs = self.client.bulbs.list()
        self.bulb_list = bulb_list
        self.bulb_list_matches = [bulb for bulb in self.bulbs if bulb.nickname in bulb_list]

    def power_off_bulb(self, device_mac, device_model):
        self.client.bulbs.turn_off(device_mac=device_mac, device_model=device_model)

    def power_on_bulb(self, device_mac, device_model):
        self.client.bulbs.turn_on(device_mac=device_mac, device_model=device_model)

    def set_color_brightness(self, device_mac, device_model, color: str, brightness: int):
        self.client.bulbs.set_brightness(device_mac=device_mac, device_model=device_model, brightness=brightness)
        self.client.bulbs.set_color(device_mac=device_mac, device_model=device_model, color=color)

    def set_bulbs_color_brightness(self, targets, color: str, brightness: int):
        threads = list()

        for bulb in targets:
            x = threading.Thread(target=self.set_color_brightness, args=(bulb.mac, bulb.product.model, color, brightness))
            threads.append(x)
            x.start()

    def power_on_bulbs(self, targets):
        threads = list()

        for bulb in targets:
            x = threading.Thread(target=self.power_on_bulb, args=(bulb.mac, bulb.product.model))
            threads.append(x)
            x.start()

    def power_off_bulbs(self, targets):
        threads = list()

        for bulb in targets:
            x = threading.Thread(target=self.power_off_bulb, args=(bulb.mac, bulb.product.model))
            threads.append(x)
            x.start()

    def get_bulbs(self, bulb_list):
        bulbs = list()
        for bulb in self.bulbs:
            if bulb.nickname in bulb_list:
                bulbs.append(bulb)

        return bulbs

    def stream_mode(self):
        ceiling_fan = ['Ceiling 1', 'Ceiling 2']
        ceiling_fan_bulbs = self.get_bulbs(ceiling_fan)

        lamp = ['Lamp']
        lamp_bulbs = self.get_bulbs(lamp)

        pink_color = 'be008e'
        blue_color = '035ffe'

        self.set_bulbs_color_brightness(ceiling_fan_bulbs, pink_color, 100)
        self.set_bulbs_color_brightness(lamp_bulbs, blue_color, 100)
        self.power_on_bulbs(ceiling_fan_bulbs + lamp_bulbs)

    def normal_mode(self):
        color = 'FBFAF5'
        self.set_bulbs_color_brightness(self.bulb_list_matches, color, 100)
        self.power_on_bulbs(self.bulb_list_matches)

    def off_mode(self):
        self.power_off_bulbs(self.bulb_list_matches)


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.dirname(os.path.abspath(__file__)) + "\\.env"
env_config = Config(RepositoryEnv(ENV_FILE))

mycontroller = WyzeController(user=env_config.get('user'),
                              password=env_config.get('password'),
                              bulb_list=['Lamp', 'Ceiling 1', 'Ceiling 2', 'Ceiling 3'])

if sys.argv[1] == "off":
    mycontroller.off_mode()

elif sys.argv[1] == "stream":
    mycontroller.stream_mode()

elif sys.argv[1] == "normal":
    mycontroller.normal_mode()
