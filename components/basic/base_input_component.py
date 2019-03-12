import logging

from components.basic.base_component import BaseComponent


class BaseInputComponent(BaseComponent):
    def __init__(self):
        super().__init__()
        self._trigger_handlers = []

    def on_trigger(self, channel):
        logging.debug("%s triggered! (Channel '%i')", self.__class__.__name__, channel)
        for handler in self._trigger_handlers:
            handler(self)

    def register_trigger_handler(self, handler):
        self._trigger_handlers.append(handler)

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
