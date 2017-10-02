from handler import Handler
from display import Display
import os
import sys

class StartUp:

    @staticmethod
    def setUp():
        Handler.display = Display(title="Multigame", width=768, height=640)
        Handler.screen = Handler.display.screen
        Handler.sep = os.sep
        Handler.mainPath = os.getcwd() + os.sep
        Handler.graphicPath = os.getcwd() + os.sep + "assets" + os.sep + "graphics" + os.sep
        Handler.soundPath = os.getcwd() + os.sep + "assets" + os.sep + "sounds" + os.sep
        #assign operating system
        os_type = None
        if "win" in sys.platform:
            os_type = "windows"
        Handler.os_type = "windows"
