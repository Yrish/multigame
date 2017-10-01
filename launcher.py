from handler import Handler

class Launcher:

    def __init__(this, url):
        Handler.serverURL = url


launch = Launcher("Hello World")
print(Handler.serverURL)
        
