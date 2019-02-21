import sys
#sys.path.insert(0, '/home/pi/Desktop/project/MFRC522python')
import logging
import RPi.GPIO as GPIO
import threading
from project.MFRC522python import SimpleMFRC522
import pickle
from datetime import datetime, timedelta
from project.folder import GLOBAL_VARIABLES

#import SimpleMFRC522

#from squid import *
#from button import Button

class rfid_class(threading.Thread):

    mode = "LISTEN"
    reader = SimpleMFRC522.SimpleMFRC522()
    allowed_tags = []
    recently_read_tags = []
   
    def handle_listen_mode(self):
        #led.set_color(GREEN)
        id = self.reader.read_id_no_block()
        logging.debug("Listen")
        if id and len(self.recently_read_tags) > 0:
            for tag in self.recently_read_tags:
                if id in tag:
                    return
            
        if id:
            if id in self.allowed_tags:
                self.recently_read_tags.append((id, datetime.now()))
                self.unlock_door()
            else:
                print("Unknown Tag")
                #flash(RED, 5, 0.1)
        #if button.is_pressed():
        #    print("pressed")
        #    self.change_mode('GRANT')

    
        
    def handle_grant_mode(self):
        #led.set_color(CYAN)
        id = self.reader.read_id_no_block()        
        if id and id not in self.allowed_tags:
            self.allowed_tags.append(id)
            self.save_tags()
            #flash(GREEN, 1, 0.1)
        #if button.is_pressed():
        #    self.change_mode('REVOKE')
            
    def handle_revoke_mode(self):
        #led.set_color(PURPLE)
        id = self.reader.read_id_no_block()
        if id and id in self.allowed_tags:
            self.allowed_tags.remove(id)
            self.save_tags()
            #flash(PURPLE, 1, 0.1)
        #if button.is_pressed():
        #    self.change_mode('LISTEN')
            
    def unlock_door(self):
        print("Door UNLOCKED")
        GLOBAL_VARIABLES.alarmed_armed = True
        
    #def flash(self, color, times, delay):
    #    for i in range(0, times):
    #        led.set_color(color)
    #        time.sleep(delay)
    #        led.set_color(OFF)
    #        time.sleep(delay) 
            
    def load_tags(self):
        try:
            with open('/home/pi/Desktop/project/data/allowed_tags.pickle', 'rb') as handle:
                self.allowed_tags = pickle.load(handle)
            print("Loaded Tags")
            print(self.allowed_tags)      
        except:
            pass
        
    def save_tags(self):
        print("Saving Tags")
        print(self.allowed_tags)
        with open('/home/pi/Desktop/project/data/allowed_tags.pickle', 'wb') as handle:
            pickle.dump(self.allowed_tags, handle)

    def check_recent_tags(self):
        for x in self.recently_read_tags:
            timestamp = datetime.now()

            dt = timestamp - x[1]
            delta_ms = dt.microseconds / 1000 + dt.seconds * 1000

            print("Time difference: ", delta_ms)

            if (delta_ms) > 1000:
                self.recently_read_tags.remove(x)
                print("Timeout for tag ", x[0])

    def change_mode(self, newMode):
        self.mode = newMode
        logging.debug("Mode changed; now ", newMode)

    def __init__(self):
        threading.Thread.__init__(self)
        pass

    def run(self):
        self.load_tags()
        try:
            while True:
                if self.mode == "LISTEN":
                    self.handle_listen_mode()
                elif self.mode == "GRANT":
                    self.handle_grant_mode()
                elif self.mode == "REVOKE":
                    self.handle_revoke_mode()
                self.check_recent_tags()
                sys.stdout.flush()
                
        finally:
            print("cleaning up")
            GPIO.cleanup()
