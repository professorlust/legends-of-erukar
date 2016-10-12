import erukar
from erukar.engine.model.Manager import Manager

class TurnManager(Manager):
    MaximumTurnCount = 100
    TurnWaitTime = 15 # sec
    TickCount = 50

    def __init__(self):
        super().__init__()
        self.current_turn_count = 0
        self.turn_order = None  # This will be a generator
        self.most_recent_active_commands = {}
        self.tick_time = False

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
        if not self.turn_order:
            return None
        next_player, self.current_turn_count = next(self.turn_order)
        return next_player

    def needs_tick(self):
        result = self.tick_time
        self.tick_time = False
        return result

    def turn_order_generator(self, current_turn_count=0):
        '''
        (Generator) Turn Order Calculator: Calculates which of the subscribed
        players should go next in turn order according to his or her dexterity modifier.
        * current_turn_count allows the system to restart the turn count if a
        lifeform dies/disconnects or joins the server.
        '''
        while True:
            current_turn_count = (current_turn_count + 1) % TurnManager.MaximumTurnCount
            if current_turn_count % self.TickCount is 0:
                self.tick_time = True
            for player in self.players:
                if (current_turn_count+1) % player.turn_modifier() == 0:
                    if player.afflicted_with(erukar.engine.effects.Dead):
                        continue
                    yield (player, current_turn_count)

    def has_players(self):
        return any([p for p in self.players if self.is_playable(p)])

    def is_playable(self, p):
        if isinstance(p, erukar.engine.model.PlayerNode):
            return not p.afflicted_with(erukar.engine.effects.Dead)
        return False
