import pygame

class Display:

    def __init__(this, **kwords):
        this.title = kwords.get("title", "Default Screen")
        this.width = kwords.get("width", 720)
        this.height = kwords.get("height", 640)
        this.screen = pygame.display.set_mode((this.width, this.height))
        pygame.display.set_caption(this.title)
