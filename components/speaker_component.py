import time

from MoreThreading import Threaded

from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent

@BuilderHint("speaker")
class SpeakerComponent(BaseComponent):
    def __init__(self):
        super().__init__()
        
        self.signal = None

    def _post_config(self):
        self.signal = self.get_pin(name = "Enable")
    
    def _do_single_beep(self, period):
        self.signal.write(1)
        time.sleep(period/2)
        self.signal.write(0)
        time.sleep(period/2)

    @Threaded
    def single_beep(self, length, frequency):
        period = 1 / frequency
        loops = int(length / period)
        for x in range(loops):
            self._do_single_beep(period)
