class Manager:
    def __init__(self):
        self.players = []

    def subscribe(self, player):
        self.players.append(player)

    def unsubscribe(self, player):
        if player in self.players:
            self.players.remove(player)

    def get_player_from_uid(self, uid):
        return next((x for x in self.players if hasattr(x, 'uid') and x.uid == uid), None)

    def get_player_from_uuid(self, uuid):
        return next((x for x in self.players if hasattr(x, 'uuid') and x.uuid == uuid), None)
