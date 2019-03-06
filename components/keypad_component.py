from xml.etree import ElementTree

from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent
from components.basic.base_input_component import BaseInputComponent
from events.events import Observe


@BuilderHint("keypad")
class KeypadComponent(BaseInputComponent):
    _keyLayout = []

    def __init__(self):
        super().__init__()

    def set_key_layout(self, layout):
        self._keyLayout = layout

    def get_key(self):
        pass


