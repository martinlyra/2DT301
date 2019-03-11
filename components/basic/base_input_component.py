import logging

from components.basic.base_component import BaseComponent


class BaseInputComponent(BaseComponent):
    trigger_handlers = []
    
    def __init__(self):
        super().__init__()

    def on_trigger(self, channel):
        print(self.__class__.__name__, "triggered! (Channel:", channel, ")")

    def scan(self):
        pass

    def register(self):
        super().register()

        count = 0
        for pin in self.pins:
            if pin.is_input():
                pin.setup_event(self.on_trigger)
                count += 1
                
        if count > 0:
            logging.debug("Registered %i event detectors for %s.", count, self.__class__.__name__)
