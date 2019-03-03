class Pin:
    pinId = ''
    pinGpio = 0
    iotype = ''
    trigger = ''

    def __init__(self, pid : str, pio : int, type : str, trigger : str):
        self.pinId = pid
        self.pinGpio = pio
        self.iotype = type
        self.trigger = trigger
