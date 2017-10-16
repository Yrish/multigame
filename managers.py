import pygame
import os
from handler import Handler
import sys

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
        Handler.currentGameState = gameState
        Handler.gameStateManager = this
        this.startGameLoop();
        this.running = None

    def startGameLoop(this):
        Handler.currentGameState.start()
        this.running = True
        while this.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    this.stop()
            Handler.display.tick()
            Handler.currentGameState.tick()
            Handler.currentGameState.render()
            Handler.display.update()

    def stop(this):
        Handler.currentGameState.stop()
        pygame.quit()
        sys.exit()
        quit()

    def pause(this):
        this.running = False

    def resume(this):
        this.startGameLaap()
