from datetime import datetime, timedelta
import time
import logging

class NormalArmedBehaviour(object):
    master = None               # type: AlarmController

    _triggered = False          # type: bool
    _sounding = False           # type: bool
    _time_triggered = None      # type: datetime

    _time_last_blink = None     # type: datetime
    
    _blink_time = timedelta(milliseconds = 250)
    _wait_time = timedelta(minutes = 0.5)

    def __init__(self, master):
        super().__init__()
        self.master = master

    def on_trigger(self):
        self._triggered = True
        self._time_triggered = datetime.now()

    def on_alarm(self):
        if self.is_triggered() is not True:
            self.on_trigger()
        self._sounding = True
        self.master.alarmLight.toggle(1)

        self.master.interfaceController.messenger.send_mail()

    def on_accepted(self):
        self._triggered = False
        self._sounding = False
        self._time_triggered = None
        self.master.alarmLight.toggle(0)

    def tick(self):
        if self._triggered:
            if self._sounding:
                self._sounding_tick()
            else:
                self._triggered_tick()

    def is_triggered(self) -> bool:
        return self._triggered

    def is_sounding(self) -> bool:
        return self._sounding

    def _triggered_tick(self):
        # Do LED blinking
        if self._time_last_blink == None:
            self._time_last_blink = datetime.now()
            self.master.alarmLight.toggle(1)
        else:
            d = datetime.now() - self._time_last_blink
            if d > self._blink_time:
                self.master.alarmLight.toggle()
                self._time_last_blink = datetime.now()

        # Keep countdown until the alarm sounds
        d = datetime.now() - self._time_triggered
        if d > self._wait_time:
            self.on_alarm()

    def _sounding_tick(self):
        self.master.sound.single_beep(0.5, 2500).join()
        time.sleep(0.25)
