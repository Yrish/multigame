import pygame
from utils import Utils
from keyHandler import Key
from keyHandler import Handler as KeyHandler

class Event:

    def __init__(this):
        pass

    def render(this):
        pass

    def tick(this):
        pass

    def start(this):
        pass

class MapKeys(Event):

    def __init__(this):
        super().__init__()
        this.started = False
        this.prompt = "press {0}."
        this.order = ["right","up","left","down","attack(A)","attack(B)","pause"]

    def tick(this):
        if not this.started:
            this.start()
        print(this.prompt.format(this.order[this.currentIndex]))
        pygamePress = pygame.key.get_pressed()
        if 1 in pygamePress and not this.__anyPressed__():
            index = pygamePress.index(1)
            key = Key(lambda: pygame.key.get_pressed()[index], this.order[this.currentIndex], origin="pygame", index=index)
            this.keyMap[this.order[this.currentIndex]] = key
            KeyHandler.addKey(key)
            this.currentIndex += 1
            if this.currentIndex >= len(this.order):
                return True
            print(this.currentIndex)
        return False


    def __anyPressed__(this):
        for key in this.keyMap.values():
            if key.isPressed():
                return True
        return False

    def start(this):
        this.started = True
        KeyHandler.clearKeys()
        this.keyMap = {}
        this.currentIndex = 0
