import logging
import time
from xml.etree import ElementTree


class TagInfo(object):
    tagId = ''
    value = 0
    user = ''
    mode = "DENY"

    def __init__(self, tid, tval, tmode, tuser=None):
        self.tagId = tid
        self.value = int(tval)
        self.user = tuser
        self.mode = tmode


class CodeInfo(object):
    codeId = ''
    value = ''

    def __init__(self, cid, cval):
        self.codeId = cid
        self.value = cval
        

class UserInfo(object):
    username = ''
    password = ''
    real_name = ''

    def __init__(self, name, word, real=None):
        self.username = name
        self.password = word
        self.real_name = real


class LoginInfo(object):
    username = ''
    password = ''

    def __init__(self, name, word):
        self.username = name
        self.password = word


class AuthController(object):
    tags = []
    codes = []
    users = []

    accept_handlers = []
    deny_handlers = []

    def __init__(self, master):
        self.master = master

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
        users = config_tree.findall('user')

        count = 0
        for user in users:
            #uid = user.get('id')
            uname = user.get('name')
            upass = user.get('pass')

            self.users.append(UserInfo(uname, upass))
            count +=1 

        logging.debug("Loaded %i user infos", count)

    def register_accept_handler(self, handler):
        self.accept_handlers.append(handler)

    def register_deny_handler(self, handler):
        self.deny_handlers.append(handler)
    
    #
    # Auth events
    #

    def _on_auth_accept(self, id, method):
        for handler in self.accept_handlers:
            handler(id, method)

    def _on_auth_deny(self, id, method):
        for handler in self.deny_handlers:
            handler(id, method)

    #
    # Authentication
    #

    def authenticate(self):
        pass    # TODO: add authentication for RFID, manual code, and remote activation via web

    def authenticate_tag(self, val):
        for tag in self.tags:
            if val == tag.value:
                self._on_auth_accept(val, "Tag")
                return
        self._on_auth_deny(val, "Tag")

    def authenticate_code(self, code):
        for code in self.code:
            if code == code.value:
                self._on_auth_accept(code, "Code")
                return
        self._on_auth_deny(code, "code")

    def authenticate_user(self, login : LoginInfo):
        for user in self.users:
            if user.username == login.username and user.password == login.password:
                self._on_auth_accept(login.username, "Login")
                return
        self._on_auth_deny(login.username, "login")
