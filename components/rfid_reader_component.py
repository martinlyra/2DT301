from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent

from MFRC522python import SimpleMFRC522

@BuilderHint("rfid-reader")
class RfidReaderComponent(BaseComponent):

    reader = SimpleMFRC522()

    on_read_tag_handlers = []

    def on_read_tag(self):
        for handler in self.on_read_tag_handlers:
            handler()

    def register_on_read_tag_callback(self, handler):
        self.on_read_tag_handlers.append(handler)

