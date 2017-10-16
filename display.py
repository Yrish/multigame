import pygame

class Display:

    def __init__(this, **kwords):
        this.title = kwords.get("title", "Default Screen")
        this.width = kwords.get("width", 720)
        this.height = kwords.get("height", 640)
        this.screen = pygame.display.set_mode((this.width, this.height))
        pygame.display.set_caption(this.title)

    def draw(this, image, **kwords):
        """
    Draw an image to the screen

    arguments:
        image - image to draw

        dictionary arguments

        pre="str"
            Acceptable commands:
                "fill_width" - width=screen_width, x=0
                "fill_height" - height=screen_height, y=0
                "fill" - width=screen_width, height=screen_height, x=0, y=0
        
        width=width_to_draw
        heigh=height_to_draw
        x=0
        y=0
        """
        image = image.convert()
        kwords["x"] = kwords.get("x",0)
        kwords["y"] = kwords.get("y",0)
        pre = kwords.get("pre", False)
        if pre:
            if pre == "fill":
                kwords["width"], kwords["height"] = this.screen.get_size()
                kwords["x"] = 0
                kwords["y"] = 0
            elif pre == "fill_width":
                kwords["width"], temp = this.screen.get_size()
                kwords["x"] = 0
            elif pre == "fill_height":
                kwords["height"], temp = this.screen.get_size()
                kwords["y"] = 0
        if not image.get_rect() == (kwords["width"],kwords["height"]):
            image = pygame.transform.scale(image, (kwords["width"], kwords["height"]))
        this.screen.blit(image, (kwords["x"],kwords["y"]))

    def update(this):
        pygame.display.update()

    def tick(this):
        this.width, this.height = this.screen.get_size()
