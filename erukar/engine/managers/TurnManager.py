import erukar
from erukar.engine.model.Manager import Manager

class TurnManager(Manager):
    MaximumTurnCount = 100
    TurnWaitTime = 15 # sec

    def __init__(self):
        super().__init__()
        self.current_turn_count = 0
        self.turn_order = None  # This will be a generator
        self.most_recent_active_commands = {}
        
    def subscribe(self, player):
        super().subscribe(player)
        self.turn_order = self.turn_order_generator(self.current_turn_count)
        self.most_recent_active_commands[player] = None

    def received_command(self, player, command):
        if isinstance(command, erukar.engine.model.ActionCommand):
            self.most_recent_active_commands[player] = command

    def pop_command(self, player):
        command = self.most_recent_active_commands[player]
        self.most_recent_active_commands[player] = None
        return command

    def next(self):
        next_player, self.current_turn_count = next(self.turn_order)
        return next_player

    def execute_turn(self):
        lifeform = self.next()
        if isinstance(lifeform, erukar.engine.model.PlayerNode):
            return self.do_player_turn(lifeform)
        return self.do_npc_turn(lifeform)

    def do_player_turn(self, player):
        pass
        # inform the player that it's his turn
        # if this is the only player, don't bother sending a message 
        # wait for TurnWaitTime
        # Execute player's most recent command

    def do_npc_turn(self, npc):
        pass

    def turn_order_generator(self, current_turn_count=0):
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
