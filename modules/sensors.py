import RPi.GPIO as GPIO
import time
#from project.folder import GLOBAL_VARIABLES

motion_flag     = 0
sound_flag      = 0
mag_one_flag    = 0
mag_two_flag    = 0

PIR_PIN = 14
SOUND_PIN = 15
MAG_ONE_PIN = 2
MAG_TWO_PIN = 3

#PIR_PIN = GLOBAL_VARIABLES.PIR_PIN
#SOUND_PIN = GLOBAL_VARIABLES.SOUND_PIN
#MAG_ONE_PIN = GLOBAL_VARIABLES.MAG_ONE_PIN
#MAG_TWO_PIN = GLOBAL_VARIABLES.MAG_TWO_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(SOUND_PIN, GPIO.IN)
GPIO.setup(MAG_ONE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MAG_TWO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
index = 0

def motion_detected(channel):
    global motion_flag
    motion_flag = 1
    print("Motion detected!!!")
    
    
def sound_detected(channel):
    global sound_flag
    sound_flag = 1
    global index
    index = index + 1
    print("Sound detected!!!", index)
    

def mag_one_detected(channel):
    if GPIO.input(MAG_ONE_PIN):
        global mag_one_flag
        mag_one_flag = 1
        print("Magnet switch one opened", mag_one_flag)
        
    else:
        print("Magnet switch one closed")
    
def mag_two_detected(channel):
    if GPIO.input(MAG_TWO_PIN):
        global mag_two_flag
        mag_two_flag = 1
        print("Magnet switch two opened")
        
    else:
        print("Magnet switch two closed")



GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)
GPIO.add_event_detect(SOUND_PIN, GPIO.RISING, callback=sound_detected)
GPIO.add_event_detect(MAG_ONE_PIN, GPIO.BOTH, callback=mag_one_detected)
GPIO.add_event_detect(MAG_TWO_PIN, GPIO.BOTH, callback=mag_two_detected)

#index = 0
#while(1):
#    index = index + 1
 #   time.sleep(1)
  #  print(index, ": ", GPIO.input(MAG_ONE_PIN))

