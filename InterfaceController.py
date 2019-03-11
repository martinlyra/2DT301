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
        self.keypad.set_key_layout(
            [['7','8','9','A'],
             ['4','5','6','B'],
             ['1','2','3','C'],
             ['*','0','#','D']])

    def setup_server(self, config_tree : ElementTree):
        self.webServer = HttpWebServer(config_tree)

    def register_rfid_read_handler(self, handler):
        self._rfid_read_handlers.append(handler)

    def on_rfid_read(self, id):
        if not id is None:
            for handler in self._rfid_read_handlers:
                handler(id)

    def run(self):
        self.webServer.start()

        while not self.is_exiting():
            #logging.debug("Interface running.")
            self.rfidReader.scan()
            time.sleep(0.5)

        self.shutdown()

    def shutdown(self):
        self.webServer.shutdown()
            
    def is_exiting(self) -> bool:
        return self.do_exit
