from handler import Handler
import pygame
import string
from time import time

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
        this.origX = kwords.get("x", None)
        this.origY = kwords.get("y", None)
        this.origWidth = kwords.get("width", None)
        this.origHeight = kwords.get("height", None)
        this.x = kwords.get("x", 0)
        this.y = kwords.get("y", 0)
        this.width = kwords.get("width", 0)
        this.height = kwords.get("height", 0)

    def getX(this):
        return this.x

    def getY(this):
        return this.y

    def getWidth(this):
        return this.width

    def getHeight(this):
        return this.height

    def setX(this, value):
        this.x = value

    def setY(this, value):
        this.y = value

    def setWidth(this, value):
        this.width = value

    def setHeight(this, value):
        this.height = value
        

    def tick(this):
        pass

    def hasFocus(this):
        return this.isFocused

    def render(this, **kwords):
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
        print(Handler.currentManagers.keys())
        this.objectManager = Handler.currentManagers["ScreenObject"].new()
        this.addElements()
        this.isFocusable = True
        this.isGroup = True

    def tick(this):
        this.objectManager.tick()

    def render(this, **kwords):
        if (this.isVisable):
            this.objectManager.render()

    def addElements(this):
        pass

    def __contains__(this, obj):
        return obj in this.objectManager

    def focusNext(this):
        return this.objectManager.focusNext()

class Window(Group):

    def __init__(this, **kwords):
        """
Class: Window
type: nonStatic
extends: ScreenObject
Args -> box

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

        objects = []
        padding = 8    The amount of autopadding between objects
        focusIndexValue = 0   The default object to focus
        """
        super().__init__(**kwords)
        this.objectManager.objects = kwords.get("objects", [])
        this.isFocusable = True
        if len(this.objectManager.objects) > 0:
            this.objectManager.removeAllFocus()
            print(this.objectManager.objects[kwords.get("focusIndexValue", 0)].requestFocus())
        this.padding = kwords.get("padding", 8)
        this.box = Box(**kwords)
        this.insetDimensions = this.box.insetDimensions()
        for i, objec in enumerate(this.objectManager.objects):
            if objec.origY == None:
                if i <= 0:
                    objec.setY(this.padding)
                else:
                    objecRef = this.objectManager.objects[i-1]
                    objec.setY(objecRef.y + objecRef.getHeight() + this.padding)

    def render(this, **kwords):
        t1 = time()
        surface = kwords.get("surface", Handler.display.screen)
        this.insetDimensions = this.box.insetDimensions()
        insetDimensions = this.insetDimensions
        insetSurface = this.__newSurface__(insetDimensions["width"], insetDimensions["height"])
        for objec in this.objectManager.objects:
            objec.render(surface=insetSurface)
        this.box.render(rendered = this.box.renderedCopy, surface = surface)
        surface.blit(insetSurface, (insetDimensions['x'], insetDimensions['y']))
        print("rendered in: " + str(time() - t1))

    def tick(this):
        t1 = time()
        this.box.tick()
        print("ticked in: " + str(time() - t1))
        for objec in this.objectManager.objects:
            objec.tick()

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

    def setY(this, value):
        this.y = value
        this.box.setY(value)

    def setX(this, value):
        this.x = value
        this.box.setX(value)

    def setWidth(this, value):
        this.width = value
        this.box.setWidth(value)

    def setHeight(this, value):
        this.height = value
        this.box.setHeight(value)

    def getHeight(this):
        return this.box.getHeight()

    def getWidth(this):
        return this.box.getWidth()

    def enter(this):
        if type(this.command).__name__ == "function":
            this.command(this)
        else:
            Handler.currentManagers["ScreenObject"].focusNext()
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

    def render(this, **kwords):
        surface = kwords.get("surface", Handler.display.screen)
        xOff, yOff = this.rendered.get_size()
        if (xOff > this.width):
            xOff = xOff - this.width
        else:
            xOff = 0
        if (yOff > this.height):
            yOff = yOff - this.height
        else:
            yOff = 0
        surface.blit(this.rendered, (this.x + this.padding, this.y + this.padding), (xOff,yOff,this.width, this.height))
        this.box.render(**kwords)
        

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
        this.textureSet = Handler.currentManagers["Asset"][kwords.get("textureSet", "BOXdefault")]
        this.margin = kwords.get("margin",8)
        this.horizontalOption = kwords.get("horizontalOption", "fill")
        this.verticalOption = kwords.get("verticalOption", "fill")
        this.lastWidth = 0
        this.lastHeight = 0
        this.lastBoxWidth = this.width
        this.lastBoxHeight = this.height
        if kwords.get("callOption", None):
            if kwords["callOption"] == "heightOfCenter":
                this.height += 2 * this.textureSet["top"].get_rect().height
        this.rendered = this.__newSurface__(this.width, this.height)
        this.renderedCopy = this.rendered.copy()
        this.tick()

    def render(this, **kwords):
        surface = kwords.get("surface", Handler.display.screen)
        rendered = kwords.get("rendered", this.rendered)
        surface.blit(rendered.convert_alpha(), (this.x, this.y))

    def tick(this):
        if Handler.display.width != this.lastWidth or Handler.display.height != this.lastHeight or this.width != this.lastBoxWidth or this.height != this.lastBoxHeight:
            this.updateImage()
            this.lastBoxWidth = this.width
            this.lastBoxHeight = this.height
            this.lastWidth = Handler.display.width
            this.lastHeight = Handler.display.height
        this.renderedCopy = this.rendered

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

    def __newSurface__(this, width, height):
        return pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()

    def insetDimensions(this):
        return {"x":this.x + this.margin + this.textureSet["topLeft"].get_rect().width, "y": this.y + this.margin + this.textureSet["topLeft"].get_rect().height, "width":this.width - 2 * this.margin - 2 * this.textureSet["topLeft"].get_rect().width, "height":this.height - 2 * this.margin - 2 * this.textureSet["topLeft"].get_rect().height}

    def __drawBox__(this, **kwords):
        this.rendered = this.__newSurface__(this.width, this.height)
        sWidth, sHeight = (this.width, this.height)#this.rendered.get_size()
        xOff = this.margin
        yOff = this.margin
        options = this.textureSet.get("options", {})
        width, height = this.textureSet["topLeft"].get_size()
        this.__drawPart__("topLeft", xOff, xOff + width, yOff, yOff + height, options.get("topLeft", "fill"))
        xOff += width
        width, height = this.textureSet["top"].get_size()
        this.__drawPart__("top",xOff, sWidth - xOff, yOff, yOff + height, options.get("top", "fill"))
        xOff = sWidth - xOff
        width, height = this.textureSet["topRight"].get_size()
        this.__drawPart__("topRight", xOff, xOff + width, yOff, yOff + height, options.get("topRight","fill"))
        yOff += height
        xOff = this.margin
        width, height = this.textureSet["left"].get_size()
        this.__drawPart__("left", xOff, xOff + width, yOff, sHeight - yOff, options.get("left","fill"))
        xOff += width
        width, height = this.textureSet["middle"].get_size()
        this.__drawPart__("middle",xOff, sWidth - xOff, yOff, sHeight - yOff, options.get("middle","fill"))
        xOff = sWidth - xOff
        width, height = this.textureSet["right"].get_size()
        this.__drawPart__("right", xOff, xOff + width, yOff, sHeight - yOff, options.get("right","fill"))
        yOff = sHeight - yOff
        xOff = this.margin
        width, height = this.textureSet["bottomLeft"].get_size()
        this.__drawPart__("bottomLeft", xOff, xOff + width, yOff, yOff + height, options.get("bottomLeft","fill"))
        xOff += width
        width, height = this.textureSet["bottom"].get_size()
        this.__drawPart__("bottom",xOff, sWidth - xOff, yOff, yOff + height, options.get("bottom","fill"))
        xOff = sWidth - xOff
        width, height = this.textureSet["bottomRight"].get_size()
        this.__drawPart__("bottomRight", xOff, xOff + width, yOff, yOff + height, options.get("bottomRight","fill"))
        

    def __drawPart__(this, dictKey,xOffmin, xOffmax, yOffmin, yOffmax, option):
        print((dictKey, xOffmin, yOffmin, xOffmax, yOffmax, xOffmax - xOffmin, yOffmax - yOffmin))
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
                print("".join(["\nhrep: ",str(hrep),"\nwrep: ",str(wrep)]))
                height = (yOffmax - yOffmin) / hrep
                width = (xOffmax - xOffmin) / wrep
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
                print("width:",width,"\nheight:",height)
                hcount = 0
                xcount = 0
                while hcount < hrep:
                    xOff = xOffmin
                    xcount = 0
                    while xcount < wrep:
                        #print(width * xcount - int(width) * xcount)
                        this.rendered.blit(pygame.transform.scale(part, (int(width), int(height))), (xOff ,yOff))
                        xcount += 1
                        xOff += int(width)
                    if int(xOffmax) > xOff:
                        this.rendered.blit(pygame.transform.scale(part, (int(width), int(height))).subsurface((0,0,int(xOffmax-xOff),int(height))), (xOff,yOff))
                    yOff += int(height)
                    hcount += 1
                return
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
        this.origX = kwords.get("x", None)
        this.y = kwords.get("y", 0)
        this.orgY = kwords.get("y", None)
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
        rendered = kwords.get("rendered", this.rendered)
        x = this.x
        y = this.y
        if this.interpretX == "right":
            x -= this.aWidth
        if this.interpretY == "bottom":
            y -= this.aHeight
        surface.blit(rendered, (x,y))

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
        this.charEnterKey = kwords.get("charEnterKey", "\n")
        this.label = Label(string=this.string, font=this.font, fontColor=this.fontColor, x=this.x + this.padding, y=this.y+this.padding)
        this.box = Box(x=this.x, y=this.y,width=this.label.rendered.get_rect().width + 2*this.padding,height=this.label.rendered.get_rect().height + 2*this.padding)

    def setY(this, value):
        this.y = value
        this.box.setY(value)

    def setX(this, value):
        this.x = value
        this.box.setX(value)

    def setWidth(this, value):
        this.width = value
        this.box.setWidth(value)

    def setHeight(this, value):
        this.height = value
        this.box.setHeight(value)
    
    def tick(this):
        pass

    def render(this, **kwords):
        pass
