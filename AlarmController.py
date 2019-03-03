from InterfaceController import InterfaceController
from SystemController import SystemController
from components.keypad_component import KeypadComponent
from ConfigController import ConfigController
from SystemBuilder import SystemBuilder
from components.rfid_reader_component import RfidReaderComponent


class AlarmController:
    configController = None     # type: ConfigController
    systemController = None     # type: SystemController
    interfaceController = None  # type: InterfaceContoller

    def __init__(self):
        self.configController = ConfigController()

        KeypadComponent()

        self.systemController = SystemController(SystemBuilder(ConfigController.config.systemConfig))
        self.interfaceController = InterfaceController()

        self.interfaceController.rfidReader = self.systemController.getFirstOf(RfidReaderComponent)
        self.interfaceController.keypad = self.systemController.getFirstOf(KeypadComponent)

    def shutdown(self):
        pass

