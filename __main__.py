from project import app

if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        print("Keyboard interrutpion recieved, shutting down.")
    app.exit()
