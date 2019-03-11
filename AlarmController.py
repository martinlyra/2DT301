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

from CameraController import CameraController
from MediaController import MediaController

class AlarmController(object):
    authController = None       # type: AuthController
    configController = None     # type: ConfigController
    systemController = None     # type: SystemController
    interfaceController = None  # type: InterfaceContoller

    sound = None
    armedLight = None
    alarmLight = None

    _exiting = False            # type: bool
    _armed = False              # type: bool

    def __init__(self):
        # Set up Configuration
        self.configController = ConfigController()

        # Set up System
        self.systemController = SystemController(SystemBuilder(ConfigController.config.systemConfig))
        self.sound = self.systemController.get_by_name('SPK')
        self.armedLight = self.systemController.get_by_name('LED0')
        self.alarmLight = self.systemController.get_by_name('LED1')

        # Set up Camera + system for images
        self.mediaController = MediaController(
            self.configController.config.primaryConfig.find('media'))
        self.cameraController = CameraController(self.mediaController)

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
        self.interfaceController.register_keypad_read_handler(self.handle_keypad_code)

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
        self.armedLight.toggle()
        return self._armed

    def on_accepted_handler(self, id, method):
        self.toggle_armed()
        self.cameraController.take_still()
        logging.debug("Alarm has been turned %s by %s using %s.",
                      "on" if self.is_armed() else "off",
                      id, method)
        self.sound.beep_short()

    def on_denied_handler(self, id, method):
        logging.debug("Authentication failed for %s using %s.", id, method)
        self.cameraController.take_still()

    def handle_sensor_trigger(self, component):
        pass

    def handle_keypad_code(self, code):
        self.authController.authenticate_code(code)

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

