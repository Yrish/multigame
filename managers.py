import pygame
import os
from handler import Handler
from keyHandler import Handler as KeyHandler
import sys
import json

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

    def __getPNG__(this, path):
        return pygame.image.load(path)

    def loadBoxTexture(this, name):
        if name == "default":
            this.assets["BOX"+name] = this.__loadBoxTextures__(Handler.defaultGraphicsPath + "Box", "default")
        else:
            this.assets["BOX"+name] = this.__loadBoxTextures__(Handler.defaultGraphicsPath + "Box", name)
            #.assets["BOX"+name] = this.__loadBoxTextures__(os.sep.join([Handler.graphicsPath,"Boxes"], name))


    def __loadBoxTextures__(this, path, name):
        with open(os.sep.join([path,name + ".dat"]), "r", encoding="utf-16") as file:
            js = json.load(file, encoding="utf-16")

        ret = {}
        ret["original"] = this.__getPNG__(os.sep.join([path,name]) + ".png")
        ret["whole"] = ret["original"].copy()

        ret.update(this.__getImagesFromJSON__(ret["whole"], js.get("cropping", {})))
        ret["options"] = js.get("contain", {}).get("options", {})

        return ret
        '''
        return {"topLeft": this.loadPNG(path, "topLeft.png"), "top": this.loadPNG(path, "top.png"), "topRight":this.loadPNG(path, "topRight.png"),
                "left": this.loadPNG(path, "left.png"), "middle": this.loadPNG(path, "middle.png"), "right":this.loadPNG(path, "right.png"),
                "bottomLeft": this.loadPNG(path, "bottomLeft.png"), "bottom": this.loadPNG(path, "bottom.png"), "bottomRight":this.loadPNG(path, "bottomRight.png")}
        '''


    def __getImagesFromJSON__(this, wholeImage, jsonMap):
        ret = {}
        for key in jsonMap:
            ret[key] = wholeImage.subsurface(jsonMap[key])
        return ret
    
    def getBoxTexture(this, name):
        if not "BOX"+name in this.assets:
            try:
                this.loadBoxTexture(name)
            except Exception as e:
                if name == "default":
                    raise e
                return this.getBoxTexture("default")
        return this.assets["BOX" + name]

    def __getitem__(this, key):
        if key.startswith("BOX"):
            return this.getBoxTexture(key.strip("BOX"))
        raise KeyError("Asset Manager can not find file: '" + str(key) + "' as no prefixes were detected")
        

class GameState:

    def __init__(this, gameState):
        Handler.currentGameState = gameState
        Handler.gameStateManager = this
        this.startGameLoop();
        this.running = None

    def startGameLoop(this):
        Handler.tickID = 0
        Handler.currentGameState.start()
        this.running = True
        while this.running:
            Handler.pygameEvents = pygame.event.get()
            KeyHandler.tick()
            print(KeyHandler.pressed)
            for event in Handler.pygameEvents:
                if event.type == pygame.QUIT:
                    this.stop()
            Handler.display.tick()
            Handler.tickID += 1
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
        this.lastNext = -1

    def requestFocus(this):
        this.isFocused = True

    def removeFocus(this):
        this.isFocused = False

    def hasFocus(this):
        if this.isFocused:
            return True
        for objec in this.objects:
            if objec.hasFocus:
                return True
        return False

    def removeAllFocus(this):
        for objec in this.objects:
            if objec.isFocused:
                if not objec.removeFocus():
                    return False
                if "isGroup" in dir(objec) and objec.isGroup:
                    objec.objectManager.removeAllFocus()

    def putFocusOn(this, obj):
        if obj in this:
            for objec in this.objects:
                if objec == obj:
                    return obj.requestFocus()
                if "isGroup" in dir(objec) and objec.isGroup:
                    if obj in objec:
                        return objec.objectManager.putFocusOn(obj)
        return False

    def focus(this, obj):
        if obj in this.objects:
            for obj in this.objects:
                obj.removeFocus();
            return this.putFocusOn(obj)
        return False

    def getFocusedObject(this):
        for objec in this.objects:
            if objec.isFocused:
                if "isGroup" in dir(objec) and objec.isGroup:
                    return objec.objectManager.getFocusedObject()
                return objec

    def hasFocusedObject(this):
        for objec in this.objects:
            if objec.isFocused:
                if "isGroup" in dir(objec) and objec.isGroup:
                    return objec.objectManager.hasFocusedObject()
                return True
            

    def __contains__(this, obj):
        for objec in this.objects:
            if obj == objec:
                return True
            if "isGroup" in dir(objec) and objec.isGroup:
                return obj in objec

    def addObject(this, obj, focus=False):
        this.objects.append(obj)
        if focus:
            this.putFocusOn(obj)

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

    def focusNext(this):
        print("Focusing Next")
        if this.lastNext == Handler.tickID:
            return False
        this.lastNext = Handler.tickID
        for i, objec in enumerate(this.objects):
            if "isGroup" in dir(objec) and objec.isGroup and objec.hasFocus():
                if objec.focusNext():
                    return True
                continue
            if objec.hasFocus():
                objec.removeFocus()
                focusIndex = i + 1
                if focusIndex >= len(this.objects):
                    focusIndex = 0
                Handler.currentManagers["ScreenObject"].putFocusOn(this.objects[focusIndex])
                print("Found: " + str(objec) + "@ index " + str(i) + " moving to " + str(this.objects[focusIndex]) + "@ index " + str(focusIndex))
                return True
        return False
