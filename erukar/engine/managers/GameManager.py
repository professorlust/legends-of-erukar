class GameManager:
    def __init__(self):
        self.players = []

    def subscribe(self, player):
        self.players.append(player)
