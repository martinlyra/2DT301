import logging

import SystemBuilder
from components.basic.base_component import BaseComponent
from components.basic.base_input_component import BaseInputComponent


class SystemController:
    components = []

    _trigger_handlers = []

    def __init__(self, system_builder : SystemBuilder):
        self.components = system_builder.buildSystem()

        logging.debug("===== Registering components =====")
        for component in self.components:
            component.register()

        self._subscribeToAll()

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

    def register_system_triggered_handler(self, handler):
        self._trigger_handlers.append(handler)
    
    def onSystemTriggered(self, component):
        for handler in self._trigger_handlers:
            handler(component)

    def _subscribeToAll(self):
        for component in self.components:
            if isinstance(component, BaseInputComponent):
                component.register_trigger_handler(self.onSystemTriggered)
                #print("Registered trigger handler to", component.__class__)

