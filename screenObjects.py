from handler import Handler

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

    def __init__(this):
        super().__init__()
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
