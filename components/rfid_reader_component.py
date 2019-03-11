from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent

from MFRC522python.SimpleMFRC522 import SimpleMFRC522


@BuilderHint("rfid-reader")
class RfidReaderComponent(BaseComponent):

    reader = SimpleMFRC522()

    on_read_tag_handlers = []
    
    def scan(self):
        id = self.reader.read_id_no_block()

        if id is not None:
            self.on_read_tag(self, id)

    def on_read_tag(self, id):
        for handler in self.on_read_tag_handlers:
            handler(id)

    def register_on_read_tag_callback(self, handler):
        self.on_read_tag_handlers.append(handler)

