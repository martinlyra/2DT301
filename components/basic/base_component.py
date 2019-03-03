from xml.etree.ElementTree import ElementTree

from components.basic.ComponentBuilder import BuilderHint
from components.basic.pin import Pin


@BuilderHint("component")
class BaseComponent:
    pins = []

    def __init__(self):
        pass

    def configure(self, config_tree: ElementTree):
        config_pins = config_tree.findall('pin')
        for cpin in config_pins:
            pid = cpin.get('id').text
            pio = int(cpin.get('gpio').text)
            iotype = cpin.get('io').text
            trigger = cpin.get('trigger').text
            self.pins.append(Pin(pid, pio, iotype, trigger))

    def register(self):
        pass

    def deregister(self):
        pass

