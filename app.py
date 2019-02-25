import sys
import time
from threading import Thread
import traceback
import RPi.GPIO as GPIO
from project.modules import rfid
from project.modules.rfid_thread_class import rfid_class
import logging
from project.folder import GLOBAL_VARIABLES
#from project.modules import sensors

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(2, GPIO.IN)

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',
                    )


def run():
    global test_armed
    init_rfid()

    #test = rfid_class()

    #test.run()

    while True:
        time.sleep(1)
        logging.debug("main loop %s", GLOBAL_VARIABLES.alarm_armed)
        pass
        

def init_rfid():
    try:
        #reader = rfid_class()
        #reader.start()
        t = rfid_class()
        t.start()
    except:
        print("Error: unable to start thread")

def is_running():
    return True

def exit():
    return
