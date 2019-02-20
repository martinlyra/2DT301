from picamera import PiCamera
import datetime
import time

def take_still():
    with PiCamera() as camera:
        time.sleep(2)
        timestamp = datetime.datetime.now()
        name = '/home/pi/Desktop/project/data/' + str(timestamp) + '.png'
        camera.capture(name)
        pass


def take_video(duration):
    with PiCamera() as camera:
        time.sleep(2)
        timestamp = datetime.datetime.now()
        name = '/home/pi/Desktop/project/data/' + str(timestamp) + '.h264'
        camera.start_recording(name)
        camera.wait_recording(duration)
        camera.stop_recording()
        pass
    
