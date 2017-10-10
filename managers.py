import pygame
import os

class Asset:

    def __init__(this):
        this.assets = {}

    def loadAsset(this, path, name):
        if path[-1] != os.sep:
            path += os.sep
        if not len(name.split(".")) != 2:
            return False
        extension = name.split(".")[1]
        if extension.lower() == "png":
            img = loadPNG(path, name)
            if img == False:
                return False
            this.assets[name] = img
            return True

    def loadPNG(this, path, name):
        if path[-1] != os.sep:
            path += os.sep
        try:
            img = pygame.image.load(path + name)
        except Exception:
            return False
        return img
