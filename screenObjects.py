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

    def __newSurface__(this, width, height):
        return pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()

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
        this.font = kwords.get("font", Handler.defaultFont)
        this.fontColor = kwords.get("fontColor", (0,0,0))
        this.padding = kwords.get("padding", 6)
        this.defocusOnEnter = kwords.get("defocusOnEnter", True)
        this.buf = list(kwords.get("string", ""))
        this.clearOnEnter = kwords.get("clearOnEnter", False)
        this.command = kwords.get("command", None)
        this.height = kwords.get("height", this.font.render("Hj", True, this.fontColor).get_rect().height)
        print(this.height)
        this.box = Box(x=this.x, y=this.y, width=this.width + this.padding * 2, height=this.height, callOption="heightOfCenter", margin=0)
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
        this.box.tick()

    def render(this):
        xOff, yOff = this.rendered.get_size()
        if (xOff > this.width):
            xOff = xOff - this.width
        else:
            xOff = 0
        if (yOff > this.height):
            yOff = yOff - this.height
        else:
            yOff = 0
        Handler.display.screen.blit(this.rendered, (this.x + this.padding, this.y + this.padding), (xOff,yOff,this.width, this.height))
        this.box.render()
        

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
        callOption = None
            "heightOfCenter"    the height is interpreted as the height of the middle of the box
        """
        
        super().__init__(**kwords)
        this.x = kwords.get("x", 0)
        this.y = kwords.get("y", 0)
        if kwords.get("width", False):
            kwords["horizontalOption"] = None
        if kwords.get("height", False):
            kwords["verticalOption"] = None
        this.width = kwords.get("width", 200)
        this.height = kwords.get("height", 100)
        this.textureSet = Handler.currentManagers["Asset"].getBoxTexture(kwords.get("textureSet", "default"))
        this.margin = kwords.get("margin",8)
        this.horizontalOption = kwords.get("horizontalOption", "fill")
        this.verticalOption = kwords.get("verticalOption", "fill")
        this.lastWidth = 0
        this.lastHeight = 0
        this.lastBoxWidth = this.width
        this.lastBoxHeight = this.height
        if kwords.get("callOption", None):
            if kwords["callOption"] == "heightOfCenter":
                print(dir(this.textureSet["top"].get_rect()))
                this.height += 2 * this.textureSet["top"].get_rect().height
        this.rendered = this.__newSurface__(this.width, this.height)
        this.tick()

    def render(this):
        Handler.display.screen.blit(this.rendered.convert_alpha(), (this.x, this.y))

    def tick(this):
        if Handler.display.width != this.lastWidth or Handler.display.height != this.lastHeight or this.width != this.lastBoxWidth or this.height != this.lastBoxHeight:
            this.updateImage()
            this.lastWidth = Handler.display.width
            this.lastHeight = Handler.display.height

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
        this.__drawBox__("repeat")

    def __newSurface__(this, width, height):
        return pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()

    def __drawBox__(this, option):
        this.rendered = this.__newSurface__(this.width, this.height)
        sWidth, sHeight = (this.width, this.height)#this.rendered.get_size()
        xOff = this.margin
        yOff = this.margin
        width, height = this.textureSet["topLeft"].get_size()
        this.__drawPart__("topLeft", xOff, xOff + width, yOff, yOff + height, "fill")
        xOff += width
        width, height = this.textureSet["top"].get_size()
        this.__drawPart__("top",xOff, sWidth - xOff, yOff, yOff + height, option)
        xOff = sWidth - xOff
        width, height = this.textureSet["topRight"].get_size()
        this.__drawPart__("topRight", xOff, xOff + width, yOff, yOff + height, "fill")
        yOff += height
        xOff = this.margin
        width, height = this.textureSet["left"].get_size()
        this.__drawPart__("left", xOff, xOff + width, yOff, sHeight - yOff, option)
        xOff += width
        width, height = this.textureSet["middle"].get_size()
        this.__drawPart__("middle",xOff, sWidth - xOff, yOff, sHeight - yOff, option)
        xOff = sWidth - xOff
        width, height = this.textureSet["right"].get_size()
        this.__drawPart__("right", xOff, xOff + width, yOff, sHeight - yOff, option)
        yOff = sHeight - yOff
        xOff = this.margin
        width, height = this.textureSet["bottomLeft"].get_size()
        this.__drawPart__("bottomLeft", xOff, xOff + width, yOff, yOff + height, "fill")
        xOff += width
        width, height = this.textureSet["bottom"].get_size()
        this.__drawPart__("bottom",xOff, sWidth - xOff, yOff, yOff + height, option)
        xOff = sWidth - xOff
        width, height = this.textureSet["bottomRight"].get_size()
        this.__drawPart__("bottomRight", xOff, xOff + width, yOff, yOff + height, "fill")
        

    def __drawPart__(this, dictKey,xOffmin, xOffmax, yOffmin, yOffmax, option):
        xOff = xOffmin
        yOff = yOffmin
        part = this.textureSet[dictKey].convert_alpha()
        width, height = part.get_size()
        if option:
            if option == "repeat":
                while yOff + height <= yOffmax:
                    while xOff + width <= xOffmax:
                        this.rendered.blit(part, (xOff, yOff))
                        xOff += width
                    if xOff <= xOffmax:
                        this.rendered.blit(part, (xOff, yOff), (0,0,xOffmax-xOff,height))
                    xOff = xOffmin
                    yOff += height
                if yOff <= yOffmax:
                    xOff = xOffmin
                    while xOff + width <= xOffmax:
                        this.rendered.blit(part, (xOff, yOff), (0,0,width,yOffmax-yOff))
                        xOff += width
                    if xOff <= xOffmax:
                        this.rendered.blit(part, (xOff, yOff), (0,0,xOffmax-xOff,yOffmax-yOff))
                return
            if option == "fullRepeat":
                hrep = float(yOffmax - yOffmin) / height
                wrep = float(xOffmax - xOffmin) / width
                print("".join(["height: ",str(height),"\nwidth: ",str(width),"\nhrep: ",str(hrep),"\nwrep: ",str(wrep)])) 
                if hrep - int(hrep) > 0.5:
                    hrep = int(hrep) + 1
                else:
                    hrep = int(hrep)
                if wrep - int(wrep) > 0.5:
                    wrep = int(wrep) + 1
                else:
                    wrep = int(wrep)
                if not (wrep and hrep):
                    return
                height = (yOffmax - yOffmin) / hrep
                width = (xOffmax - xOffmin) / wrep
                hcount = 0
                xcount = 0
                while hcount < hrep:
                    xOff = xOffmin
                    hcount += 1
                    xcount = 0
                    while xcount < wrep:
                        xcount += 1
                        this.rendered.blit(pygame.transform.scale(part, (int(width), int(height))), (xOff,yOff))
                        xOff += width
                    yOff += height
        this.rendered.blit(pygame.transform.scale(part, (int(xOffmax - xOff), int(yOffmax - yOff))), (xOff, yOff))

class Label(ScreenObject):

    def __init__(this, **kwords):
        super().__init__(**kwords)
        """
    class: Label
    type: nonstatic
    extends: ScreenObject

    Args (key words):
        string=""   the string to display
        x=0         x position of draw
        y=0         y position of draw
        interpretX="left"
            "left"  x is interpreted as the far left x position
            "right" x is interpreted as the far right x position
        interpretY="top"
            "top"     y is interpreted as the top of the label
            "bottom"  y is interpreted as the bottom of the label
        width="auto"
            "auto"    width extends as far as necesary to fit text
            numeric   a number of pixels which the label extends
        height="auto"
            "auto"   height extends as far as necessary to fit text
            numeric  a number of pixels which the label extends down
        font=Handler.defaultFont
        fontColor = (0,0,0)
        """
        this.string = kwords.get("string", "")
        this.x = kwords.get("x", 0)
        this.y = kwords.get("y", 0)
        this.interpretX = kwords.get("interpretX", "left")
        this.interpretY = kwords.get("interpretY", "top")
        this.width = kwords.get("width", "auto")
        this.height = kwords.get("height", "auto")
        this.font = kwords.get("font",Handler.defaultFont)
        this.fontColor = kwords.get("fontColor", (0,0,0))
        this.lastString = None
        this.rendered = this.__newSurface__(10,10)
        this.aWidth = 0
        this.aHeight = 0
        this.tick()

    def tick(this):
        if this.string != this.lastString:
            this.updateRender()

    def updateRender(this):
        renderedString = this.font.render(this.string, True, this.fontColor).convert_alpha()
        if this.width == "auto":
            width = renderedString.get_rect().width
        else:
            width = this.width
        if this.height == "auto":
            height = renderedString.get_rect().height
        else:
            height = this.height
        this.aWidth = width
        this.aHeight = height
        this.rendered = this.__newSurface__(width, height)
        this.rendered.blit(renderedString, (0,0), (0,0,width,height))
        

    def render(this, **kwords):
        surface = kwords.get("surface", Handler.display.screen)
        x = this.x
        y = this.y
        if this.interpretX == "right":
            x -= this.aWidth
        if this.interpretY == "bottom":
            y -= this.aHeight
        surface.blit(this.rendered, (x,y))

class Button(ScreenObject):

    def __init__(this, **kwords):
        """
    class: Button
    type: nonStatic
    extends: ScreenObject

    args (keyword):
        necessary args:
            pressComand=function  command called when pressed (called as function(caller, *positionalArgs, **kwordArgs)
        string=""
        x=0
        y=0
        interpretX="left"
            "left"  x is interpreted as the far left x position
            "right" x is interpreted as the far right x position
        interpretY="top"
            "top"     y is interpreted as the top of the label
            "bottom"  y is interpreted as the bottom of the label
        font=Handler.defaultFont
        fontColor=(0,0,0)
        padding = 8   the amount of pixels between the text and the box
        this.positionalArgs=()
        this.kwordArgs={}
        """
        super().__init__(**kwords)
        if not "pressCommand" in kwords:
            raise ValueError("keyword argument \"pressCommand\" must be defined")
        if type(kwords["pressCommand"]) != 'function':
            raise TypeError('argument for keywords \"pressCommand\" must be of type \'function\'')
        this.x = kwords.get("x",0)
        this.y = kwords.get("y",0)
        this.interpretX = kwords.get("interpretX", "left")
        this.interpretY = kwords.get("interpretY", "top")
        this.string = kwords.get("string","")
        this.font = kwords.get("font", Handler.defaultFont)
        this.fontColor= kwords.get("fontColor", (0,0,0))
        this.padding = kwords.get("padding",8)
        this.positionalArgs = kwords.get("positionalArgs", ())
        this.kwordArgs = kwords.get("kwordArgs", {})
        this.label = Label(string=this.string, font=this.font, fontColor=this.fontColor, x=this.x + this.padding, y=this.y+this.padding)
        this.box = Box(x=this.x, y=this.y,width=this.label.rendered.get_rect().width + 2*this.padding,height=this.label.rendered.get_rect().height + 2*this.padding)
        
    def tick(this):
        pass

    def render(this, **kwords):
        pass
