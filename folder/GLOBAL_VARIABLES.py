
# These variables represent the pins that we are using for diffrent things.
# They, the variables, are constant and should not be changed. 
PIR_PIN = 14
SOUND_PIN = 15
MAG_ONE_PIN = 2
MAG_TWO_PIN = 3
PIEZO_PIN = 14

# Other stuff
alarm_armed = False
alarm = False

#alarm_armed = 0
#alarm       = 0

def is_armed():
    return alarm_armed

def is_triggered():
    return alarm
