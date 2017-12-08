import pygame
from handler import Handler as overHandler

class Key:

    def __init__(this, pressCondition, key, **special_info):
        this.key = key
        this.pressCondition = pressCondition
        this.specialInfo = special_info

    def isPressed(this):
        return this.pressCondition()

class Handler:
    """
    Static class: works with user inputs
    """

    pastPressed = {}
    pressed = {}
    articulate = {}
    __staticArticulate__ = {}
    __keyPast__ = {}
    keys = {}
    
    @staticmethod
    def tick():
        Handler.pastPressed = Handler.pressed
        Handler.pressed = dict(Handler.pressed)
        Handler.__keyPast__ = dict((key, value.isPressed()) for key, value in Handler.keys.items())
        for event in overHandler.pygameEvents:
            if event.type == pygame.KEYDOWN:
                Handler.pressed[event.unicode.encode("utf-16")] = event.scancode
            elif event.type == pygame.KEYUP:
                try:
                    Handler.removeByValue(Handler.pressed,event.scancode)
                except ValueError:
                    pass
        Handler.articulate = dict((key, True) for key in Handler.getPressed())
        Handler.__staticArticulate__ = dict(Handler.articulate)
        print(Handler.isPressed("right"))

    @staticmethod
    def removeByValue(dictionary, value):
        for key in dictionary:
            if dictionary[key] == value:
                del dictionary[key]
                return
    
    @staticmethod
    def isPressed(string):
        return string in Handler.pressed or Handler.__silentKeyPressed__(string)

    def __silentKeyPressed__(string):
        try:
            return Handler.keys[string].isPressed()
        except KeyError:
            return False

    def __silentKeyJustPressed__(string):
        try:
            return Handler.keys[string].isPressed() and not Handler.__keyPast__[string].isPressed()
        except KeyError:
            return False

    def __silentKeyJustReleased__(string):
        try:
            return not Handler.keys[string].isPressed() and Handler.__keyPast__[string].isPressed()
        except KeyError:
            return False

    def __silentKeyReleased__(string):
        try:
            return not Handler.keys[string].isPressed()
        except KeyError:
            return False

    def isReleased(string):
        return not string in Handler.pressed or Handler.__silentKeyReleased__(string)

    def justPressed(string):
        return (string in Handler.pressed and not string in Handler.pastPressed) or Handler.__silentKeyJustPressed__(string)

    def justReleased(string):
        return (not string in Handler.pressed and string in Handler.pastPressed) or Handler.__silentKeyJustReleased__(string)

    def getJustPressed():
        return [key for key in Handler.pressed if not key in Handler.pastPressed] + [key for key in Handler.keys if Handler.__silentKeyJustPressed__(key)]

    def getJustReleased():
        return [key for key in Handler.pastPressed if not key in Handler.pressed] + [key for key in Handler.keys if Handler.__silentKeyJustReleased__(key)]

    def getPressed():
        return list(Handler.keys.keys()) + list(Handler.keys.keys())

    def getArticulateJustPressed():
        return [key for key in Handler.articulate if not key in Handler.pastPressed]

    def getArticulateJustReleased():
        return [key for key in Handler.pastPressed if not key in Handler.__staticArticulate__]

    def setKeys(keyDict):
        Handler.keys = keyDict

    def clearKeys():
        Handler.keys = {}

    def addKey(key):
        Handler.keys[key.key] = key

    def __delitem__(this, key):
        try:
            del pressed[key]
        except KeyError:
            pass
