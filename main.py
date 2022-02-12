import sys
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError


class WyzeController:
    def __init__(self, user, password, bulb_list):
        self.client = Client(email=user, password=password)
        self.bulbs = self.client.bulbs.list()
        self.bulb_list = bulb_list

    def power_off_office_lights(self):
        for bulb in self.bulbs:
            if bulb.nickname in self.bulb_list:
                self.client.bulbs.turn_off(device_mac=bulb.mac, device_model=bulb.product.model)

    def stream_mode(self):
        ceiling_fan = ['Ceiling 1', 'Ceiling 2']
        lamp = ['Lamp']

        pink_color = 'be008e'
        blue_color = '035ffe'

        for bulb in self.bulbs:
            if bulb.nickname in ceiling_fan:
                self.client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color=pink_color)
                self.client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model, brightness=100)
                self.client.bulbs.turn_on(device_mac=bulb.mac, device_model=bulb.product.model)
            elif bulb.nickname in lamp:
                self.client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color=blue_color)
                self.client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model, brightness=100)
                self.client.bulbs.turn_on(device_mac=bulb.mac, device_model=bulb.product.model)

    def normal_mode(self):
        lighting_group = ['Ceiling 1', 'Ceiling 2', 'Lamp']
        color = 'FBFAF5'

        for bulb in self.bulbs:
            if bulb.nickname in lighting_group:
                self.client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color=color)
                self.client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model, brightness=100)
                self.client.bulbs.turn_on(device_mac=bulb.mac, device_model=bulb.product.model)


mycontroller = WyzeController(user=sys.argv[2], password=sys.argv[3], bulb_list=['Lamp', 'Ceiling 1', 'Ceiling 2'])

if sys.argv[1] == "off":
    mycontroller.power_off_office_lights()

elif sys.argv[1] == "stream":
    mycontroller.stream_mode()

elif sys.argv[1] == "normal":
    mycontroller.normal_mode()
