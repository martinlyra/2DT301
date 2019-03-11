from threading import Thread

import logging
import time
from xml.etree import ElementTree

from HttpWebServer import HttpWebServer
from components.keypad_component import KeypadComponent
from components.rfid_reader_component import RfidReaderComponent


class InterfaceController(Thread):
    rfidReader = None           # type: RfidReaderComponent
    keypad = None               # type: KeypadComponent
    webServer = None            # type: HttpWebServer

    do_exit = False             # type: bool

    _rfid_read_handlers = []    # type: list
    _keypad_read_handlers = []  # type: list

    def set_rfid(self, rfid):
        self.rfidReader = rfid
        self.rfidReader.register_on_read_tag_callback(self.on_rfid_read)

    def set_keypad(self, keypad):
        self.keypad = keypad

    def setup_server(self, config_tree : ElementTree):
        self.webServer = HttpWebServer(config_tree)

    def register_rfid_read_handler(self, handler):
        self._rfid_read_handlers.append(handler)

    def on_rfid_read(self, id):
        if not id is None:
            for handler in self._rfid_read_handlers:
                handler(id)

    def run(self):
        self.webServer.run()

        while not self.is_exiting():
            #logging.debug("Interface running.")
            self.rfidReader.scan()
            self.keypad.scan()
            time.sleep(1)

        self.shutdown()

    def shutdown(self):
        self.webServer.shutdown()
            
    def is_exiting(self) -> bool:
        return self.do_exit
