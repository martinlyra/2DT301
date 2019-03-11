import RPi.GPIO as GPIO

from xml.etree.ElementTree import ElementTree

def _get_value_or_default(value, default):
    type = default.__class__
    if value is not None:
        if value is not type:
            return type(value)
        else:
            return value
    else:
        return default

class Pin(object):
    pinId = ''
    pinGpio = 0
    iotype = ''
    pud = 'down'
    trigger = None
    state = None
    bouncetime = 1

    def __init__(self, config_tree : ElementTree):
        config = config_tree
        
        self.pinId = config.get('id')
        self.pinGpio = int(config.get('gpio'))
        self.iotype = config.get('io')

        self.pud = _get_value_or_default(config.get('pud'), 'down').lower()
        self.bouncetime = _get_value_or_default(config.get('bouncetime'), 1)
        self.trigger = _get_value_or_default(config.get('trigger'), 'both').lower()
        self.state = _get_value_or_default(config.get('state'), 'low').lower() 

    def write(self, value):
        if self.is_output():
            GPIO.output(self.pinGpio, value)
            #print("Output pin", self.pinGpio,"now set to",value)

    def read(self):
        if self.is_input():
            inp = GPIO.input(self.pinGpio)
            if inp == GPIO.HIGH:
                return 1
            return 0

    def setup(self):
        io = GPIO.OUT
        if self.iotype == "in":
            io = GPIO.IN

        pud = GPIO.PUD_DOWN
        if self.pud == 'up':
            pud = GPIO.PUD_UP

        #print("Setting up pin", self.pinGpio, "for", self.iotype)
        if self.is_input():
            GPIO.setup(self.pinGpio, io, pull_up_down=pud)

        if self.is_output():
            GPIO.setup(self.pinGpio, io)
            
            if self.state == "high":
                self.write(1)
            elif self.state == "low":
                self.write(0)

    def setup_event(self, handler):
        trigger = None
        if self.trigger == "rising":
            trigger = GPIO.RISING
        elif self.trigger == "falling":
            trigger = GPIO.FALLING
        else:
            trigger = GPIO.BOTH
        
        GPIO.add_event_detect(self.pinGpio, trigger, callback=handler,
                              bouncetime=self.bouncetime)

        #print("Event handler of type",trigger,"registered at",self.pinGpio)

    def is_input(self) -> bool:
        return self.iotype == 'in'

    def is_output(self) -> bool:
        return self.iotype == 'out'

        
        
