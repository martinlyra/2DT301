import RPi.GPIO as GPIO
from project.MFRC522python import SimpleMFRC522

import project.folder.identities as iden

reader = SimpleMFRC522.SimpleMFRC522()
GPIO.setwarnings(False)

def write_tag():
    try:
        text = input('Write the data you would like to write to the tag: ')
        print("Place the tag next to the device.")
        nr = reader.read_id()
        reader.write(text)
        iden.rfid_tag_1 = (nr, text)
        print("Done")
    finally:
        GPIO.cleanup()

def read_tag():
    try:
        print("Place the tag next to the device.")
        id, text = reader.read()
        print(id)
        print(text)
    finally:
        GPIO.cleanup()
