import logging

from AlarmController import AlarmController

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',
                    )

if __name__ == '__main__':
    alarm = AlarmController()
    try:
        alarm.run()
    except Exception:
        pass
    alarm.shutdown()

