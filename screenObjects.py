from handler import Handler
import pygame
import string

class ScreenObject:

    def __init__(this, **kwords):
        """
    Object which is rendered to the screen

    Args:
        keyword args:
            zIndex = 0  -Higher zIndexes will apear on top
            isAlive = True -Keeps the object on the screen
            isFocused = False -Focus of screen (only one focus at a time)
            isFocusable = False -If object can obtain focus
            isPersistant = False -If object should pertain focus even if requested to lose it
            isVisable = True -Renders the object
            grouping = Handler.currentManagers["Assets"] -If the objects pertains to a custom group, like a window
        """
        this.zIndex = kwords.get("zIndex", 0)
        this.isAlive = kwords.get("isAlive", True)
        this.isFocused = kwords.get("isFocused", False)
        this.isFocusable = kwords.get("isFocusable", True)
        this.isPersistant = kwords.get("isPersistant", False)
        this.isVisable = kwords.get("isVisable", True)
        this.isGroup = False
        

    def tick(this):
        pass

    def render(this):
        pass

    def requestFocus(this):
        if this.isFocusable:
            this.isFocused = True
            return True
        this.isFocused = False

    def removeFocus(this):
        if not this.isPersistant:
            this.isFocused = False
            return True
        return False

class Group(ScreenObject):

    def __init__(this, **kwords):
        super().__init__(**kwords)
        this.objectManager = Handler.currentManagers["ScreenObjects"].new()
        this.addElements()
        this.isFocusable = False
        this.isGroup = True

    def tick(this):
        this.objectManager.tick()

    def render(this):
        if (this.isVisable):
            this.objectManager.render()

    def addElements(this):
        pass

    def __contains__(this, obj):
        return obj in this.objectManager

class Window(Group):

    def __init__(this):
        super().__init__()
        this.isFocusable = True
        Handler.currentManagers["ScreenObjects"].focus(this)

class textInputBox(ScreenObject):

    AcceptableInputs = string.printable

    def __init__(this, **kwords):
        """
        Class: textBox
        type: noneStatic
        extends: ScreenObject

        x = 0    x position
        y = 0    y position
        width = 100    width of textbox
        height = 50    height of textbox
        font = font    font used to display text (pygame)
        fontColor = (0,0,0)  color the font is displayed in
        padding = 6   offset of text from perimeter
        defocusOnEnter = True   defocuses the object when enter is pressed
        command = None    command run on enter
        string = ""    string originally displayed run as command(self)
        clearOnEnter = False  removes text from string if true
        """
        super().__init__(**kwords)
        this.x = kwords.get("x",0)
        this.y = kwords.get("y",0)
        this.width = kwords.get("width", 100)
        this.height = kwords.get("height",50)
        this.font = kwords.get("font", Handler.defaultFont)
        this.fontColor = kwords.get("fontColor", (0,0,0))
        this.padding = kwords.get("padding", 6)
        this.defocusOnEnter = kwords.get("defocusOnEnter", True)
        this.buf = list(kwords.get("string", ""))
        this.clearOnEnter = kwords.get("clearOnEnter", False)
        this.command = kwords.get("command", None)
        #data
        this.string = None
        this.tick()

    def enter(this):
        if type(this.command).__name__ == "function":
            this.command(this)
        else:
            this.removeFocus()
        if this.clearOnEnter:
            this.string = ""

    def tick(this):
        #event handling
        for event in Handler.pygameEvents:
            if event.type == pygame.KEYDOWN and this.isFocused:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    this.enter()
                elif event.key == pygame.K_BACKSPACE:
                    if this.buf:
                        this.buf.pop()
                elif event.unicode in textInputBox.AcceptableInputs:
                    this.buf.append(event.unicode)
            #Mouse curser click
            '''
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                this.focused = this.rect.collidepoint(event.pos)
            '''
        new = "".join(this.buf)
        print(new)
        if new != this.string:
            this.string = new
            this.rendered = this.font.render(this.string, True, this.fontColor)
            '''
            this.rendRect = this.rendered.get_rect(x=this.x,y=this.y)
            if this.rendRect.width > this.width - this.padding:
                off = this.width - (this.width - this.padding)
                this.rendArea = pygame.Rect(off,0,this.width - this.padding, this.rendRect.height)
            else:
                this.rendArea = this.rendered.get_rect(topleft=(0,0))
            '''
        #blinking

    def render(this):
        Handler.display.screen.blit(this.rendered, (this.x, this.y))
        

class Box(ScreenObject):

    def __init__(this, **kwords):
        """
Class: Box
type: nonStatic
extends: ScreenObject

    Args:
        x=0
        y=0
        width=200
        height=100
        margin = 8   width/height away from the sides of the screen (if applicable)
        textureSet=default
        horizontalOption= fill
            "fill"      the width = width of window
            "center"    the x = center of screen
            None
        verticalOption= bottom
            "fill"       the height = height of screen
            "center"     the y = center of screen
            "top"        the y = align to top of screen
            "bottom"     the y = align to bottom of screen
            None         don't do anything
        """
        
        super(kwords)
        this.x = kwords.get("x", 0)
        this.y = kwords.get("y", 0)
        this.width = kwords.get("width", 200)
        this.height = kwords.get("height", 100)
        this.textureSet = handler.currentManagers["Asset"].getBoxTexture(kwords.get("textureSet", "default"))
        this.margin = kwords.get("margin",8)
        this.horizontalOption = kwords.get("horizontalOption", "fill")
        this.verticalOption = kwords.get("verticalOption", "fill")
        this.lastWidth = 0
        this.lastHeight = 0
        this.rendered = pygame.Surface((this.width, this.height))

    def render(this):
        pass

    def tick(this):
        if Handler.display.width != this.lastWidth or Handler.display.height != this.lastHeight:
            this.updateImage()

    def updateImage(this):
        if this.horizontalOption:
            if this.horizontalOption == "fill":
                this.width = Handler.display.width
                this.x = 0
            elif this.horizontalOption == "center":
                this.x = Handler.display.width / 2 - this.width / 2
        if this.verticalOption:
            if this.verticalOption == "fill":
                this.height = Handler.display.height
                y = 0
            elif this.verticalOption == "center":
                this.y = Handler.display.height / 2 - this.height / 2
            elif this.verticalOption == "top":
                this.y = 0
            elif this.verticalOption == "bottom":
                this.y = Handler.display.height - this.height
        this.__drawBox__()

    def __drawBox__(this):
        this.rendered = pygame.Surface((this.width, this.height))
        xOff = this.margin
        yOff = this.margin

    def __drawPart__(dictKey,xOffmin, xOffmax, yOffmin, yOffmax, option):
        xOff = xOffmin
        yOff = yOffmin
        part = this.textureSet[dictKey]
        width, height = part.get_size()
        if option:
            if option == "repeat":
                while yOff + height <= yOffmax:
                    while xOff + width <= xOffmax:
                        this.rendered.blit(part, (xOff, yOff))
                        xOff += width
                    if xOff <= xOffmax:
                        this.rendered.blit(part, (xOff, yOff), (0,0,xOffMax-xOff,height))
                    xOff = xOffmin
                    yOff += height
                if this.yOff <= yOffmax:
                    xOff = xOffmin
                    while xOff + width <= xOffmax:
                        this.rendered.blit(part, (xOff, yOff), (0,0,width,yOffmax-yOff))
                        xOff += width
                    if xOff <= xOffmax:
                        this.rendered.blit(part, (xOff, yOff), (0,0,xOffMax-xOff,yOffmax-yOff))
                return
            if option == "contain":
                          
        this.rendered.blit(pygame.transform.scale(part, xOffmax - xOff, yOffmax - yOff), (xOff, yOff))
        
