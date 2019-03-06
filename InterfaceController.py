from threading import Thread

import logging
import time

from components.keypad_component import KeypadComponent
from components.rfid_reader_component import RfidReaderComponent


class InterfaceController(Thread):
    rfidReader = None       # type: RfidReaderComponent
    keypad = None           # type: KeypadComponent

    do_exit = False

    _rfid_read_handlers = []
    _keypad_read_handlers = []

    def set_rfid(self, rfid):
        self.rfidReader = rfid
        self.rfidReader.register_on_read_tag_callback(self.on_rfid_read)

    def set_keypad(self, keypad):
        self.keypad = keypad

    def register_rfid_read_handler(self, handler):
        self._rfid_read_handlers.append(handler)

    def on_rfid_read(self, id):
        if not id is None:
            for handler in self._rfid_read_handlers:
                handler(id)

    def run(self):
        while not self.is_exiting():
            #logging.debug("Interface running.")
            self.rfidReader.handle_read()
            time.sleep(1)
            
    def is_exiting(self) -> bool:
        return self.do_exit
