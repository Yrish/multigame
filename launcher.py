import pygame
pygame.init()
from handler import Handler
from startup import StartUp
from gameStates import Load

class Launcher:

    def __init__(this, url):
        Handler.serverURL = url
        StartUp.setUp()
        Load()


launch = Launcher("Hello World")
print(Handler.serverURL)
print(Handler.mainPath)
print(Handler.graphicsPath)
print(Handler.soundPath)
print(Handler.os_type)
        
