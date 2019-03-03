import logging
import xml.etree.ElementTree


class Config:
    defaultConfigFolder = "config/" # type: str

    authorizationConfigName = "Authorization.xml"  # type: str
    primaryConfigName = "Config.xml"  # type: str
    systemConfigName = "System.xml"  # type: str

    authConfig = None  # type: ElementTree
    systemConfig = None  # type: ElementTree
    primaryConfig = None  # type: ElementTree


class ConfigController:
    config = Config()  # type: Config

    def __init__(self):
        self.config.primaryConfig = xml.etree.ElementTree.parse(
            self.config.defaultConfigFolder + self.config.primaryConfigName).getroot()

        primary = self.config.primaryConfig

        links = primary.findall('link')
        for link in links:
            target = link.get('target')
            if target == "auth":
                self.config.authorizationConfigName = link.get('file')
            elif target == "system":
                self.config.systemConfigName = link.get('file')
            else:
                logging.debug("Unknown link target in configuration: %s", target)

        self.config.authConfig = xml.etree.ElementTree.parse(
            self.config.defaultConfigFolder + self.config.authorizationConfigName).getroot()
        self.config.systemConfig = xml.etree.ElementTree.parse(
            self.config.defaultConfigFolder + self.config.systemConfigName).getroot()

