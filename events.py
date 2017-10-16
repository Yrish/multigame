import pygame

class Event:

    def __init__(this):
        pass

    def render(this):
        pass

    def tick(this):
        pass

class MapKeys(Event):

    def __init__(this):
        super().__init__()
        this.started = False
        this.prompt = "press right."
        this.order = ["right","up","left","down","attack(A)","attack(B)","pause"]

    def tick(this):
        if not this.started:
            this.start()
        print(this.prompt)

    def start(this):
        this.keyMap = {}
