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
        this.startGameLoop()

    def switchGameState(this, gameState):
        Handler.currentManagers = {"Asset":Asset(),"ScreenObject":ScreenObject()}
        Handler.currentGameState = gameState
        gameState.init()

class ScreenObject:

    def __init__(this):
        this.isFocused = True
        this.objects = []

    def requestFocus(this):
        this.isFocused = True

    def removeFocus(this):
        this.isFocused = False

    def removeAllFocus(this):
        for objec in this.objects:
            if objec.isFocused:
                if not objec.removeFocus():
                    return False
                if "isGroup" in dir(objec) and objec.isGroup:
                    if obj in objec:
                        objec.objectManager.removeAllFocus()

    def putFocusOn(this, obj):
        if obj in this:
            for objec in this.objects:
                if objec == obj:
                    return obj.requestFocus()
                if "isGroup" in dir(objec) and objec.isGroup:
                    if obj in objec:
                        objec.objectManager.putFocusOn(obj)

    def focus(this, obj):
        if obj in this:
            this.removeAllFocus()
            return this.putFocusOn(obj)
        return False
            

    def __contains__(this, obj):
        for objec in this.objects:
            if obj == objec:
                return True
            if "isGroup" in dir(objec) and objec.isGroup:
                return obj in objec

    def addObject(this, obj):
        this.objects.append(obj)

    def removeObject(this, obj):
        this.objects.remove(obj)

    def removeDeadObjects(this):
        for obj in this.objects:
            if not obj.isAlive:
                this.objects.remove(obj)

    def tick(this):
        for obj in this.objects:
            obj.tick()
        this.removeDeadObjects()

    def render(this):
        for obj in this.objects:
            obj.render()

    def new(this):
        return ScreenObject()
        
