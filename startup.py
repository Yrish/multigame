from handler import Handler
from display import Display
from webSupport import WebSupport
import pygame
import os
import sys

class StartUp:

    @staticmethod
    def setUp():
        Handler.display = Display(title="Multigame", width=768, height=640)
        Handler.screen = Handler.display.screen
        Handler.sep = os.sep
        Handler.mainPath = os.getcwd() + os.sep
        Handler.graphicsPath = os.getcwd() + os.sep + "assets" + os.sep + "graphics" + os.sep
        Handler.boxPath = Handler.graphicsPath + os.sep + "box" + os.sep
        Handler.soundPath = os.getcwd() + os.sep + "assets" + os.sep + "sounds" + os.sep
        Handler.entitiesPath = Handler.mainPath + os.sep + "entities" + os.sep
        Handler.defaultGraphicsPath = Handler.graphicsPath + "default" + os.sep
        Handler.screenShotsPath = Handler.mainPath + os.sep + "ScreenShots" + os.sep
        #assign operating system
        os_type = None
        if "win" in sys.platform:
            os_type = "windows"
        elif "linux" == sys.platform:
            if os.uname()[1] == "raspberrypi":
                os_type = "raspi"
            else:
                os_type = "linux"
        Handler.os_type = os_type
        Handler.pygameEvents = []
        Handler.defaultFont = pygame.font.Font(None, 25)
        sys.path.append(Handler.entitiesPath)
        #For testing
        WebSupport.startSession()
