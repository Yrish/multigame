import pygame
pygame.init()
from handler import Handler
from startup import StartUp

class Launcher:

    def __init__(this, url):
        Handler.serverURL = url
        StartUp.setUp()


launch = Launcher("Hello World")
print(Handler.serverURL)
print(Handler.mainPath)
print(Handler.graphicPath)
print(Handler.soundPath)
        
