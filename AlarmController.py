import logging
from xml.etree import ElementTree

from InterfaceController import InterfaceController
from SystemController import SystemController
from components.keypad_component import KeypadComponent
from ConfigController import ConfigController
from SystemBuilder import SystemBuilder
from components.rfid_reader_component import RfidReaderComponent


class TagInfo:
    tagId = ''
    value = ''
    user = ''
    mode = "DENY"

    def __init__(self, tid, tval, tmode, tuser=None):
        self.tagId = tid
        self.value = tval
        self.user = tuser
        self.mode = tmode



class CodeInfo:
    codeId = ''
    value = ''

    def __init__(self, cid, cval):
        self.codeId = cid
        self.value = cval


class UserInfo:
    username = ''
    password = ''
    real_name = ''


class AuthController(object):
    tags = []
    codes = []
    users = []

    def configure(self, config_tree: ElementTree):
        self._setup_tags(config_tree.find('rfid-tags'))
        self._setup_codes(config_tree.find('codes'))
        self._setup_users(config_tree.find('users'))

    def _setup_tags(self, config_tree: ElementTree):
        tags = config_tree.findall('tag')

        count = 0
        for tag in tags:
            tid = tag.get('id')
            tval = tag.get('value')
            tmode = tag.get('mode')
            self.tags.append(TagInfo(tid, tval, tmode))
            count += 1

        logging.debug("Loaded %i RFID tags", count)

    def _setup_codes(self, config_tree: ElementTree):
        codes = config_tree.findall('code')

        count = 0
        for code in codes:
            cid = code.get('id')
            cval = code.get('value')
            self.codes.append(CodeInfo(cid, cval))
            count += 1

        logging.debug("Loaded %i manual codes", count)

    def _setup_users(self, config_tree: ElementTree):
        pass

    def authenticate(self):
        pass    # TODO: add authentication for RFID, manual code, and remote activation via web

    def authenticate_tag(self):
        pass

    def authenticate_code(self):
        pass

    def authenticate_user(self):
        pass


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
        self.authController = AuthController()
        self.authController.configure(self.configController.config.authConfig)

        # Set up the user interface
        self.interfaceController = InterfaceController()

        self.interfaceController.rfidReader = self.systemController.getFirstOf(RfidReaderComponent)
        self.interfaceController.keypad = self.systemController.getFirstOf(KeypadComponent)

        for component in self.systemController.components:
            print(component.__class__.__name__, component)

    def is_armed(self) -> bool:
        return self._armed

    def toggle_armed(self):
        self._armed = not self._armed
        return self._armed

    def on_verified_handler(self, id, method):
        self.toggle_armed()
        logging.debug("Alarm has been turned %s by %s using %s.",
                      "on" if self.is_armed() else "off",
                      id, method)

    def run(self):
        self.interfaceController.run()

        while not self.is_exiting():
            try:
                pass
            except KeyboardInterrupt:
                self._exiting = True

        self.shutdown()

    def is_exiting(self) -> bool:
        return self._exiting

    def shutdown(self):
        self.interfaceController.join()

        self.systemController.cleanup()

