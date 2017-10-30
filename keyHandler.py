import pygame


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


    @staticmethod
    def isPressed(key):
        return False
