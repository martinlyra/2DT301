import logging


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',
                    )

def oldCode():
    import project.app as app
    
    app.run()

def newCode():
    from AlarmController import AlarmController
    
    alarm = AlarmController()
    alarm.run()
    #alarm.shutdown()

if __name__ == '__main__':
    newCode()
