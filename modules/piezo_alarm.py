import RPi.GPIO as GPIO
import time

import sys
sys.path.insert(0, '/home/pi/Desktop/project/folder/')

import GLOBAL_VARIABLES

# This line of code works if the module is run from the main script
#from project.folder import GLOBAL_VARIABLES

PIEZO_PIN = GLOBAL_VARIABLES.PIEZO_PIN

_PERIOD = 0.0004
_BEEP_LENGTH = 0.5
_BEEP_DELAY = 0.5
_BEEP_LOOPS = int(_BEEP_LENGTH/_PERIOD)
_WARNING_TIME = int(15 / (_BEEP_DELAY + _BEEP_LENGTH))

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIEZO_PIN, GPIO.OUT)
GPIO.setwarnings(False)
#GPIO.output(PIEZO_PIN, GPIO.HIGH)

def beep():
    for x in range(_BEEP_LOOPS):
        GPIO.output(PIEZO_PIN, GPIO.HIGH)
        time.sleep(_PERIOD/2)
        GPIO.output(PIEZO_PIN, GPIO.LOW)
        time.sleep(_PERIOD/2)


def alarm():
    while GLOBAL_VARIABLES.is_triggered():
        beep()
        time.sleep(_BEEP_DELAY)

alarm()
GPIO.cleanup()


