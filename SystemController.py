import logging

import SystemBuilder
from components.basic.base_component import BaseComponent


class SystemController:
    components = []

    def __init__(self, system_builder : SystemBuilder):
        self.components = system_builder.buildSystem()

        logging.debug("===== Registering components =====")
        for component in self.components:
            component.register()

        logging.debug("_____ _____ _____ _____ _____ _____")

    def get_by_name(self, name):
        for component in self.components:
            if component.name == name:
                return component

    def getAllOf(self, cls) -> list:
        out = []
        for component in self.components:
            if component.__class__ is cls:
                out.append(component)
        return out


    def getFirstOf(self, cls):
        res = self.getAllOf(cls)
        if len(res) > 0:
            return res[0]
        return None

    def cleanup(self):
        for component in self.components:
            component.unregister()

