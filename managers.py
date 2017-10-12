import pygame
import os
from handler import Handler

class Asset:

    def __init__(this):
        this.assets = {}

    def loadAsset(this, path, name):
        print("loading: " + name)
        if path[-1] != os.sep:
            path += os.sep
        if len(name.split(".")) != 2:
            return False
        extension = name.split(".")[1]
        print(extension)
        if extension.lower() == "png":
            img = this.loadPNG(path, name)
            if img == False:
                return False
            this.assets[name] = img
            return True

    def loadPNG(this, path, name):
        if path[-1] != os.sep:
            path += os.sep
        try:
            print("loading image path: " + path + name)
            img = pygame.image.load(path + name)
        except Exception:
            return False
        return img

class GameState:

    def __init__(this, gameState):
        Handler.current_game_state = gameState
        Handler.game_state_manager = this
        this.startGameLoop();

    def startGameLoop(this):
        while True:
            Handler.current_game_state.tick()
            Handler.current_game_state.render()
    
