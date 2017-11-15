import pygame

class MessageBoard:

    path = "messageboard/"

    def __init__(this, typ, screen, x=0, y=0, width=0, height=0, pad=10, mode=(None,None)):
        this.mode = mode
        this.x = x
        this.y = y
        this.screen = screen
        this.height = height
        this.width = width
        
        this.pad = pad
        this.typ = typ
        this.topRight = pygame.image.load(MessageBoard.path + typ + "/topRight.png")
        this.top = pygame.image.load(MessageBoard.path + typ + "/top.png")
        this.topLeft = pygame.image.load(MessageBoard.path + typ + "/topLeft.png")
        this.left = pygame.image.load(MessageBoard.path + typ + "/left.png")
        this.bottomLeft = pygame.image.load(MessageBoard.path + typ + "/bottomLeft.png")
        this.bottom = pygame.image.load(MessageBoard.path + typ + "/bottom.png")
        this.bottomRight = pygame.image.load(MessageBoard.path + typ + "/bottomRight.png")
        this.right = pygame.image.load(MessageBoard.path + typ + "/right.png")
        this.fill = pygame.image.load(MessageBoard.path + typ + "/fill.png")

    def render(this):
        width = this.width
        height = this.height
        pad = this.pad
        screen = this.screen
        mode = this.mode
        screenWidth = screen.get_rect()[2]
        screenHieght = screen.get_rect()[3]
        x = this.x
        y = this.y
        if width == "fit":
            width = screen.get_rect()[2] - 2 * this.pad
        if height == "fit":
            height = screen.get_rect()[3] - 2 * this.pad
        if width < this.topRight.get_rect()[2] + this.top.get_rect()[2] + this.topLeft.get_rect()[2]:
            width = this.topRight.get_rect()[2] + this.top.get_rect()[2] + this.topLeft.get_rect()[2]
        if height < this.topRight.get_rect()[3] + this.right.get_rect()[3] + this.bottomRight.get_rect()[3]:
            height = this.topRight.get_rect()[3] + this.right.get_rect()[3] + this.bottomRight.get_rect()[3]
        if this.mode[0] == "center":
            x = (screenWidth/2) - (width/2)
        elif this.mode[0] == "right":
            x = screenWidth - width - this.pad
        elif this.mode[0] == "left":
            x = this.pad
        if this.mode[1] == "center":
            y = (screenHieght/2) - (height/2)
        elif this.mode[1] == "bottom":
            y = screenHieght - height - this.pad
        elif this.mode[1] == "top":
            y = this.pad
        #Drawing
        xOff = x
        yOff = y
        midWidthScale = int(width - (this.topLeft.get_rect()[2] + this.topRight.get_rect()[2]))
        midHeightScale = int(height- (this.topLeft.get_rect()[3] + this.bottomLeft.get_rect()[3]))
        screen.blit(this.topLeft, (xOff, yOff))
        xOff += this.topLeft.get_rect()[2]
        screen.blit(pygame.transform.scale(this.top, (midWidthScale, int(this.top.get_rect()[3]))),(xOff,yOff))
        xOff = x + width - this.topRight.get_rect()[2]
        screen.blit(this.topRight, (xOff, yOff))
        xOff = x
        yOff = y + this.topLeft.get_rect()[3]
        screen.blit(pygame.transform.scale(this.left, (int(this.left.get_rect()[2]), midHeightScale)),(xOff,yOff))
        xOff += this.left.get_rect()[2]
        screen.blit(pygame.transform.scale(this.fill, (midWidthScale, midHeightScale)),(xOff,yOff))
        xOff += midWidthScale
        screen.blit(pygame.transform.scale(this.right, (int(this.right.get_rect()[2]), midHeightScale)),(xOff,yOff))
        yOff += midHeightScale
        xOff = x
        screen.blit(this.bottomLeft, (xOff, yOff))
        xOff += this.bottomLeft.get_rect()[2]
        screen.blit(pygame.transform.scale(this.bottom, (midWidthScale, int(this.top.get_rect()[3]))),(xOff,yOff))
        xOff += midWidthScale
        screen.blit(this.bottomRight, (xOff, yOff))
