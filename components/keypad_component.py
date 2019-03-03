from xml.etree import ElementTree

from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent
from components.basic.base_input_component import BaseInputComponent
from events.events import Observe


@BuilderHint("keypad")
class KeypadComponent(BaseInputComponent):
    def __init__(self):
        super().__init__()

        self.onKeyPressed()

    @Observe("onKeyPressed")
    def onKeyPressed(self):
        pass


