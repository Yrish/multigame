import pygame
from handler import Handler as overHandler

class Key:

    def __init__(this, pressCondition, **special_info):
        this.pressCondition = pressCondition
        this.specialInfo = special_info

    def isPressed(this):
        return this.pressCondition()

class Handler:
    """
    Static class: works with user inputs
    """

    PastPressed = []
    Pressed = []
    
    @staticmethod
    def tick():
        Handler.PastPressed = Handler.Pressed
        Handler.Pressed = list(Handler.Pressed)
        for event in overHandler.pygameEvents:
            if event.type == pygame.KEYDOWN:
                Handler.Pressed.append(event.unicode.encode("utf-16"))
            elif event.type == pygame.KEYUP:
                try:
                    print(event)
                    Handler.Pressed.remove(event.unicode.encode("utf-16"))
                except ValueError:
                    pass
    
    @staticmethod
    def isPressed(string):
        return string in Handler.Pressed

    def isReleased(string):
        return not string in Handler.Pressed

    def justPressed(string):
        return string in Handler.Pressed and not string in Handler.PastPressed

    def justReleased(string):
        return not string in Handler.Pressed and string in Handler.PastPressed
