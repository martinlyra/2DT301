import RPi.GPIO as GPIO

from xml.etree.ElementTree import ElementTree

class Pin(object):
    pinId = ''
    pinGpio = 0
    iotype = ''
    trigger = None
    state = None

    def __init__(self, config_tree : ElementTree):
        config = config_tree
        
        self.pinId = config.get('id')
        self.pinGpio = int(config.get('gpio'))
        self.iotype = config.get('io')
        
        trigger = config.get('trigger')
        state = config.get('state')

        if not trigger is None:
            self.trigger = trigger.lower()
            print 

        if not state is None:
            self.state = state.lower()

    def write(self, value):
        if self.is_output():
            GPIO.output(self.pinGpio, value)
            print("Output pin", self.pinGpio,"now set to",value)

    def setup(self):
        io = GPIO.OUT
        if self.iotype == "in":
            io = GPIO.IN

        #print("Setting up pin", self.pinGpio, "for", self.iotype)
        GPIO.setup(self.pinGpio, io)

        if self.is_output():
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
        
        GPIO.add_event_detect(self.pinGpio, trigger, callback=handler)

        #print("Event handler of type",trigger,"registered at",self.pinGpio)

    def is_input(self) -> bool:
        return self.iotype == 'in'

    def is_output(self) -> bool:
        return self.iotype == 'out'

        
        
