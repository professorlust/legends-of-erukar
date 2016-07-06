class TurnManager:
    MaximumTurnCount = 100

    def __init__(self):
        self.current_turn_count = 0
        self.players = []

    def subscribe(self, player):
        self.players.append(player)

    def turn_order(self, current_turn_count=0):
        '''
        (Generator) Turn Order Calculator: Calculates which of the subscribed 
        players should go next in turn order according to his or her dexterity modifier.
        * current_turn_count allows the system to restart the turn count if a
        lifeform dies/disconnects or joins the server.
        '''
        while True:
            current_turn_count = (current_turn_count + 1) % TurnManager.MaximumTurnCount
            for player in self.players:
                if (current_turn_count+1) % player.turn_modifier() == 0:
                    yield (player, current_turn_count)
            
