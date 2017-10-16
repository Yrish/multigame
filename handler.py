from managers import Asset as AssetManager

class Handler:

    serverURL = None
    display = None
    screen = None
    mainPath = None
    current_managers = {}
    current_game_state = None

    def startGameState():
        pass

    def switch_game_state(gameState):
        current_managers = {}
        Handler.current_managers["Asset"] = AssetManager()
        this.current_game_state = gameState
