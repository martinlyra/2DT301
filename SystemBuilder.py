import logging
from xml.etree import ElementTree

from components.basic.ComponentBuilder import valid_components


class SystemBuilder:
    config = None   # type: ElementTree
    valid_components = []   # type: list

    def __init__(self, config_tree: ElementTree):
        self.config = config_tree
        self.valid_components = valid_components

    def buildSystem(self) -> list:
        components = []
        component_configs = self.config.find('components')

        for component_config in component_configs:
            for tuple in valid_components:
                if component_config.tag == tuple[0]:
                    component = tuple[1]()
                    component.configure(component_config)
                    components.append(component)
                else:
                    logging.debug("Unknown system XML tag in configuration: %s", component_config.tag)

        return components
