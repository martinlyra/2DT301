import SystemBuilder
from components.basic.base_component import BaseComponent


class SystemController:
    components = []

    def __init__(self, system_builder : SystemBuilder):
        components = system_builder.buildSystem()

    def getAllOf(self, cls) -> list:
        out = []
        for component in self.components:
            if component is cls:
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

