import sys
import time
from threading import Thread
import traceback
import RPi.GPIO as GPIO
from project.modules import rfid
from project.modules.rfid_thread_class import rfid_class
#from project.modules import sensors


#GPIO.setmode(GPIO.BCM)
#GPIO.setup(2, GPIO.IN)


def run():
    #init_rfid()

    test = rfid_class

    test.run(test)

    #while True:
     #   time.sleep(1)
      #  print("main loop")
       # pass
        

def init_rfid():
    try:
        t = Thread(target=rfid_class, args=(""))
        t.start()
    except:
        print("Error: unable to start thread")

def is_running():
    return True

def exit():
    return
