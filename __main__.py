from AlarmController import AlarmController

if __name__ == '__main__':
    try:
        AlarmController()
    except KeyboardInterrupt:
        print("Keyboard interrutpion recieved, shutting down.")

