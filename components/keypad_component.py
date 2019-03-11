import time
from xml.etree import ElementTree

from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent
from components.basic.base_input_component import BaseInputComponent
from events.events import Observe


@BuilderHint("keypad")
class KeypadComponent(BaseInputComponent):
    _keyLayout = []

    _outpins = []
    _inpins = []

    _current_output_pin = 0

    _on_key_handlers = []

    def __init__(self):
        super().__init__()

    def configure(self, config_tree : ElementTree):
        super().configure(config_tree)

        for pin in self.pins:
            if pin.is_output():
                self._outpins.append(pin)
            elif pin.is_input():
                self._inpins.append(pin)

    def on_trigger(self, channel):
        #super().on_trigger(channel)
        self.on_key(self._get_key(channel))

    def register_on_key_handler(self, handler):
        self._on_key_handlers.append(handler)

    def on_key(self, key):
        for handler in self._on_key_handlers:
            handler(key)

    def _scan_for_intersection(self, col):
        for i in range(len(self._outpins)):
            self._outpins[i].write(1)
            val = self._inpins[col].read()
            self._outpins[i].write(0)

            if val == 1:
                return i
    
    def _get_key(self, channel):
        x = self._get_column_num(channel)
        y = self._scan_for_intersection(x)

        return self._keyLayout[x][y]

    def _get_column_num(self, channel):
        return self._get_axis_num(self._inpins, channel)

    def _get_row_num(self, channel):
        return self._get_axis_num(self._outpins, channel)

    def _get_axis_num(self, axis_list, target):
        num = 0
        for pin in axis_list:
            if pin.pinGpio == int(target):
                return num
            else:
                num += 1


    def set_key_layout(self, layout):
        self._keyLayout = layout


