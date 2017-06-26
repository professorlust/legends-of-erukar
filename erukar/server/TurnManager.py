import erukar
from erukar.engine.model.Manager import Manager

class TurnManager(Manager):
    TickIndicator = '5 Second Tick'
    MaximumTurnCount = 100000
    TickCount = 50
    MinimumOnDeck = 3

    def __init__(self):
        super().__init__()
        self.most_recent_active_commands = {}
        self.current_turn_count = 0
        self.previous_player = None
        self.active_player = None
        self.on_deck = [] 

    def subscribe(self, player):
        super().subscribe(player)
        if self.active_player is None:
            self.active_player = player
        self.refresh_deck()

    def unsubscribe(self, player):
        super().unsubscribe(player)
        self.refresh_deck()

    def received_command(self, player, command):
        if isinstance(command, erukar.engine.model.ActionCommand):
            self.most_recent_active_commands[player] = command

    def pop_command(self, player):
        command = self.most_recent_active_commands[player]
        self.most_recent_active_commands[player] = None
        return command

    def next(self):
        while len(self.on_deck) > 0:
            self.previous_player = self.active_player
            self.active_player = self.on_deck.pop(0)
            if len(self.on_deck) < self.MinimumOnDeck:
                self.refresh_deck()
            if not isinstance(self.active_player, str) and self.active_player.lifeform().is_incapacitated():
                continue
            return self.active_player

    def refresh_deck(self):
        if len(self.players) < 1: 
            raise Error("Not enough players")
            return
        while len(self.on_deck) < TurnManager.MinimumOnDeck:
            self.current_turn_count = (self.current_turn_count + 1) % TurnManager.MaximumTurnCount
            if self.current_turn_count % self.TickCount == 0:
                self.on_deck.append(TurnManager.TickIndicator)
            for player in self.players:
                mod = player.lifeform().turn_modifier()
                if (self.current_turn_count+1) % mod == 0:
                    self.on_deck.append(player)

    def has_players(self):
        return any([p for p in self.players if self.is_playable(p)])

    def is_playable(self, p):
        if isinstance(p, erukar.engine.model.PlayerNode):
            return not p.has_condition(erukar.engine.conditions.Dead)
        return False

    def frontend_readable_turn_order(self):
        turn_order = [self.previous_player, self.active_player] + self.on_deck
        return [TurnManager.to_str(x) for x in turn_order]

    def to_str(player):
        if not player: return 'N/A'
        return player if isinstance(player, str) else player.lifeform().name
