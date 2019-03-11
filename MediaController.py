import datetime
import glob
import os
import logging

from xml.etree import ElementTree


class Image(object):
    def __init__(self, file, timestamp, camera_id, description):
        self.file = file
        self.timestamp = timestamp,
        self.camid = camera_id
        self.description = description

    def from_xml(xml_tree : ElementTree):
        path = xml_tree.find('path').text
        description = xml_tree.find('description').text

        info = xml_tree.find('info')
        timestamp = info.get('time-stamp')
        cid = int(info.get('camera-id'))

        return Image(path, timestamp, cid, description)
        
    def to_xml(self):
        root = ElementTree.Element("data")
        path = ElementTree.SubElement(root, 'path')
        info = ElementTree.SubElement(root, 'info')
        description = ElementTree.SubElement(root, 'description')

        path.text = self.file
        info.set('time-stamp', str(self.timestamp))
        info.set('camera-id', str(self.camid))
        description.text = self.description

        return root


class MediaController(object):

    folder = "log/media/"

    images = []

    def __init__(self, config_tree : ElementTree):
        self.folder = config_tree.get('directory')
        self._load_all_images()

    def _load_all_images(self):
        count = 0
        for filename in glob.glob(os.path.join(self.folder, '*.xml')):
            r = ElementTree.parse(filename).getroot()
            self.images.append(Image.from_xml(r))
            count += 1
        logging.debug("Loaded information for %i images.", count)

    def add_image(self, img : Image):
        self.images.append(img)
        self._write_xml_to_file(img)

    def _write_xml_to_file(self, img : Image):
        x = ElementTree.ElementTree(element= img.to_xml())
        x.write(self.folder + str(img.timestamp) + '.xml')
    
