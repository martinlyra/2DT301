import time

from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent


@BuilderHint("speaker")
class SpeakerComponent(BaseComponent):
    def beep_short(self):
        for pin in self.pins:
            if pin.is_output():
                pin.write(1)
                time.sleep(1)
                pin.write(0)
