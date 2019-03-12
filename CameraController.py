from picamera import PiCamera
from datetime import datetime
from MoreThreading import Threaded
import time
import logging

from MediaController import MediaController, Image

class CameraController(object):
    media_controller = None
    
    destination = ''
    subfolder_img = "raw/"
    file_format_still = 'png'

    camera = None
    _camera_ready = False
    _camera_init_timetamp = None
    _warm_up_time = 2 # seconds

    def __init__(self, media_controller):
        self.camera = PiCamera()
        self._camera_init_timestamp = datetime.now()

        self.media_controller = media_controller
        self.destination = self.media_controller.folder

    @Threaded
    def take_still(self, description : str = ''):
        timestamp = datetime.now()

        filename = self.destination + self.subfolder_img + str(timestamp) + '.' + self.file_format_still

        while self._is_camera_ready() == False:
            time.sleep(0.5)
        
        self.camera.capture(filename)

        self.media_controller.add_image(Image(filename, timestamp, 1, description))
        logging.debug("Still photo has been taken!")

    def _is_camera_ready(self):
        if self._camera_ready == False:
            now = datetime.now()
            delta = now - self._camera_init_timestamp
            if delta.total_seconds() >= self._warm_up_time:
                self._camera_ready = True
        return self._camera_ready
        
        
                
        
        
