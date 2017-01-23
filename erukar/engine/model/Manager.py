class Manager:
    def __init__(self):
        self.players = []

    def subscribe(self, player):
        self.players.append(player)

    def unsubscribe(self, player):
        if player in self.players:
            self.players.remove(player)
