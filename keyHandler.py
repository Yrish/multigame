import pygame
from handler import Handler as overHandler

class Key:

    def __init__(this, pressCondition, **special_info):
        this.pressCondition = pressCondition
        this.specialInfo = special_info

    def ispressed(this):
        return this.pressCondition()

class Handler:
    """
    Static class: works with user inputs
    """

    pastPressed = {}
    pressed = {}
    articulate = {}
    __staticArticulate__ = {}
    
    @staticmethod
    def tick():
        Handler.pastPressed = Handler.pressed
        Handler.pressed = dict(Handler.pressed)
        for event in overHandler.pygameEvents:
            if event.type == pygame.KEYDOWN:
                Handler.pressed[event.unicode.encode("utf-16")] = event.scancode
            elif event.type == pygame.KEYUP:
                try:
                    print(event)
                    Handler.removeByValue(Handler.pressed,event.scancode)
                except ValueError:
                    pass
        Handler.articulate = dict(Handler.pressed)
        Handler.__staticArticulate__ = dict(Handler.articulate)
        print("\n".encode("utf-16"))
        print(Handler.isPressed("\n".encode("utf-16")))

    @staticmethod
    def removeByValue(dictionary, value):
        for key in dictionary:
            if dictionary[key] == value:
                del dictionary[key]
                return
    
    @staticmethod
    def isPressed(string):
        return string in Handler.pressed

    def isReleased(string):
        return not string in Handler.pressed

    def justPressed(string):
        return string in Handler.pressed and not string in Handler.pastPressed

    def justReleased(string):
        return not string in Handler.pressed and string in Handler.pastPressed

    def getJustPressed():
        return [key for key in Handler.pressed if not key in Handler.pastPressed]

    def getJustReleased():
        return [key for key in Handler.pastPressed if not key in Handler.pressed]

    def getArticulateJustPressed():
        return [key for key in Handler.articulate if not key in Handler.pastPressed]

    def getArticulateJustReleased():
        return [key for key in Handler.pastPressed if not key in Handler.__staticArticulate__]

    def __delitem__(this, key):
        try:
            del pressed[key]
        except KeyError:
            pass
