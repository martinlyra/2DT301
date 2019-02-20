import RPi.GPIO as GPIO
from project.MFRC522python import SimpleMFRC522

import project.folder.identities as iden

reader = SimpleMFRC522.SimpleMFRC522()
GPIO.setwarnings(False)

def read_tag():
    try:
        id, text = reader.read()
    finally:
        GPIO.cleanup

    print(id)
    print(text)
    print("asdfghjk")

    if(id == iden.rfid_tag_1[0] and text.strip() == iden.rfid_tag_1[1]):
        print("Succes")
        #
        # Deactivate alarm
        #
    else:
        print("Failure")

