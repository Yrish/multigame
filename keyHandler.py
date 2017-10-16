import pygame

class Key:

    def __init__(this, pressCondition, **special_info):
        this.pressCondition = pressCondition
        this.specialInfo = special_info

    def isPressed(this):
        return this.pressCondition()
