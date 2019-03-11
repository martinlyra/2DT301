import logging
import time
from xml.etree import ElementTree

from AuthController import AuthController
from InterfaceController import InterfaceController
from SystemController import SystemController
from components.keypad_component import KeypadComponent
from ConfigController import ConfigController
from SystemBuilder import SystemBuilder
from components.rfid_reader_component import RfidReaderComponent

class AlarmController(object):
    authController = None       # type: AuthController
    configController = None     # type: ConfigController
    systemController = None     # type: SystemController
    interfaceController = None  # type: InterfaceContoller

    _exiting = False            # type: bool
    _armed = False              # type: bool

    def __init__(self):
        # Set up Configuration
        self.configController = ConfigController()

        # Set up System
        self.systemController = SystemController(SystemBuilder(ConfigController.config.systemConfig))

        # Set up Authentication
        self.authController = AuthController(self)
        self.authController.configure(self.configController.config.authConfig)
        self.authController.register_accept_handler(self.on_accepted_handler)
        self.authController.register_deny_handler(self.on_denied_handler)

        # Set up the user interface
        self.interfaceController = InterfaceController()

        self.interfaceController.set_rfid(self.systemController.getFirstOf(RfidReaderComponent))
        self.interfaceController.set_keypad(self.systemController.getFirstOf(KeypadComponent))
        self.interfaceController.setup_server(self.configController.config.systemConfig.find('server'))
        
        self.interfaceController.register_rfid_read_handler(self.handle_rfid_tag)

        print(len(self.systemController.components),"components built from system configuration.")
        for component in self.systemController.components:
            print('\t',component.__class__.__name__)

    #
    # Alarm functions
    #
    
    def is_armed(self) -> bool:
        return self._armed

    def toggle_armed(self):
        self._armed = not self._armed
        return self._armed

    def on_accepted_handler(self, id, method):
        self.toggle_armed()
        logging.debug("Alarm has been turned %s by %s using %s.",
                      "on" if self.is_armed() else "off",
                      id, method)

    def on_denied_handler(self, id, method):
        logging.debug("Authentication failed for %s using %s.", id, method)

    def handle_rfid_tag(self, id):
        self.authController.authenticate_tag(id)

    #
    # Program flow functions
    #

    def run(self):
        logging.debug("====== STARTING RUNTIME LOOP ======")
        
        self.interfaceController.start()

        # print("Starting to run.")
        while not self.is_exiting():
            try:
                # logging.debug("Run.")
                time.sleep(1)
                # pass
            except KeyboardInterrupt:
                logging.debug("Interrupted by keyboard. Exiting.")
                self._exiting = True
                self.interfaceController.do_exit = True
            except Exception as ex:
                print(ex)

        self.shutdown()

    def is_exiting(self) -> bool:
        return self._exiting

    def shutdown(self):
        self.interfaceController.join()

        self.systemController.cleanup()

