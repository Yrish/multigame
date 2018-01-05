from managers import Asset as AssetManager
import pygame
from handler import Handler
from utils import Utils
import events as ev
from screenObjects import textInputBox, Window, Label

class GameState:

    def __init__(this):
        this.entities = []
        this.background = []
        pass

    def tick(this):
        pass

    def render(this):
        pass

    def stop(this):
        pass

    def save(this):
        pass

    def stop(this):
        pass

    def start(this):
        pass

    def init(this):
        pass

class Load(GameState):

    def __init__(this):
        super().__init__()
        Handler.currentManagers["Asset"] = AssetManager()
        this.loadAssets()
        this.keys = ev.MapKeys()
        this.keys.start()

    def loadAssets(this):
        assetManager = Handler.currentManagers["Asset"]
        assetManager.loadAsset(Handler.defaultGraphicsPath, "load_screen.png")

    def render(this):
        Handler.display.draw(Handler.currentManagers["Asset"].assets["load_screen.png"],pre="fill")
        this.keys.render()

    def tick(this):
        if this.keys.tick():
            Handler.gameStateManager.switchGameState(Menue())


class Menue(GameState):

    def __init__(this):
        super().__init__()

    def init(this):
        this.loadAssets()
        Handler.currentManagers["ScreenObject"].lastNext = Handler.tickID
        Handler.currentManagers['ScreenObject'].addObject(Window(objects=[textInputBox(string="Hello Neil!"),textInputBox(string="Hello World!"), Label(string = "Hi there")], textureSet="BOXgreen"), focus=True)

    def loadAssets(this):
        print(Handler.currentManagers["Asset"].loadAsset(Handler.defaultGraphicsPath, "opening_screen.png"))

    def render(this):
        Handler.display.draw(Handler.currentManagers["Asset"].assets["opening_screen.png"],pre="fill")
        Handler.currentManagers["ScreenObject"].render()

    def tick(this):
        Handler.currentManagers["ScreenObject"].tick()
        
    
        
        
