from threading import Thread

from components.keypad_component import KeypadComponent
from components.rfid_reader_component import RfidReaderComponent


class InterfaceController(Thread):
    rfidReader = None       # type: RfidReaderComponent
    keypad = None           # type: KeypadComponent

    pass