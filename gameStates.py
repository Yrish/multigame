from managers import Asset as AssetManager
from handler import Handler

class GameState:

    assets = []

    def __init__(this):
        pass

    def tick(this):
        pass

    def render(this):
        pass

    def stop(this):
        pass

    def save(this):
        pass

class Load(GameState):

    def __init__(this):
        super().__init__()
        Handler.current_managers["Asset"] = AssetManager()
        this.loadAssets()

    def loadAssets(this):
        assetManager = Handler.current_managers["Asset"]
        print(assetManager.loadAsset(Handler.defaultGraphicsPath, "load_screen.png"))

    def render(this):
        print(Handler.current_managers["Asset"].assets)
        Handler.display.draw(Handler.current_managers["Asset"].assets["load_screen.png"],pre="fill")
