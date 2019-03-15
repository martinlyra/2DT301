from threading import Thread

import logging
import time
from xml.etree import ElementTree

from SmtpMessenger import SmtpMessenger
from HttpWebServer import HttpWebServer
from components.keypad_component import KeypadComponent
from components.rfid_reader_component import RfidReaderComponent


class InterfaceController(Thread):
    rfidReader = None           # type: RfidReaderComponent
    keypad = None               # type: KeypadComponent
    webServer = None            # type: HttpWebServer
    messenger = None            # type: SmtpMessenger

    do_exit = False             # type: bool

    _rfid_read_handlers = []    # type: list
    _keypad_read_handlers = []  # type: list

    _key_buffer = ''

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
        self.keypad.register_on_key_handler(self.on_key_press)

    def setup_server(self, config_tree : ElementTree):
        self.webServer = HttpWebServer(config_tree)

    def setup_messenger(self, config_tree : ElementTree):
        self.messenger = SmtpMessenger(config_tree)

    def register_keypad_read_handler(self, handler):
        self._keypad_read_handlers.append(handler)

    def register_rfid_read_handler(self, handler):
        self._rfid_read_handlers.append(handler)

    def on_keypad_read(self, content):
        if content is not None:
            for handler in self._keypad_read_handlers:
                handler(content)

    def on_rfid_read(self, id):
        if not id is None:
            for handler in self._rfid_read_handlers:
                handler(id)

    def on_key_press(self, key):
        if key == '#':
            print('Code submitted: ', self._key_buffer)
            self.on_keypad_read(self._key_buffer)
            self._key_buffer = ''
        elif key == '*':
            self._key_buffer = ''
            print('Code input cleared!')
        else:
            self._key_buffer += key
            print(self._key_buffer)

    def run(self):
        self.webServer.start()

        while not self.is_exiting():
            #logging.debug("Interface running.")
            self.rfidReader.scan()
            time.sleep(0.25)

        self.shutdown()

    def shutdown(self):
        self.webServer.shutdown()
            
    def is_exiting(self) -> bool:
        return self.do_exit
