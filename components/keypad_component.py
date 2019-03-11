import time
from xml.etree import ElementTree

from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent
from components.basic.base_input_component import BaseInputComponent
from events.events import Observe


@BuilderHint("keypad")
class KeypadComponent(BaseInputComponent):
    _keyLayout = []

    _outPins = []
    _inPins = []

    _current_output_pin = 0

    def __init__(self):
        super().__init__()

        for pin in self.pins:
            if pin.is_output():
                self._outPins.append(pin)
            elif pin.is_input():
                self._inPins.append(pin)

    def on_trigger(self, channel):
        super().on_trigger(channel)
        self._get_key(channel)

    def scan(self):
        for pin in self._outPins:
            self._current_output_pin = pin.pinGpio
            pin.write(1)
            time.sleep(0.1)
            pin.write(0)

    def _get_key(self, channel):
        x = self._get_column_num(channel)
        y = self._get_row_num(channel)

        r = self._keyLayout[x][y]

        print(r)

    def _get_column_num(self, channel):
        return self._get_axis_num(self._inPins, channel)

    def _get_row_num(self, channel):
        return self._get_axis_num(self._outPins, channel)

    def _get_axis_num(self, axis_list, target):
        num = 0
        for pin in axis_list:
            if pin.pinGpio == target:
                return num
            else:
                num += 1


    def set_key_layout(self, layout):
        self._keyLayout = layout


