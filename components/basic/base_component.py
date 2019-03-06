import RPi.GPIO as GPIO
import logging

from xml.etree.ElementTree import ElementTree

from components.basic.ComponentBuilder import BuilderHint
from components.basic.pin import Pin


@BuilderHint("component")
class BaseComponent(object):

    def __init__(self):
        self.pins = []

    def configure(self, config_tree: ElementTree):
        config_pins = config_tree.find('pins')
        pins = config_pins.findall('pin')
        logging.debug("Found %i pins for %s.", len(pins), self.__class__.__name__)
        for cpin in pins:
            self.pins.append(Pin(cpin))

    def register(self):
        for pin in self.pins:
            pin.setup()
        logging.debug("%i pins setup for %s", len(self.pins) ,self.__class__.__name__)

    def unregister(self):
        GPIO.cleanup()

