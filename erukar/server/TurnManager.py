import erukar
from erukar.engine.model.Manager import Manager

import logging
logger = logging.getLogger('debug')

class TurnManager(Manager):
    TickIndicator = '5 Second Tick'
    MaximumTurnCount = 100000
    TickCount = 50
    MinimumOnDeck = 3

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.current_turn_count = 0
        self.previous_player = None
        self.active_player = None
        self.on_deck = [] 

    def subscribe(self, player):
        super().subscribe(player)
        logger.info('TurnManager -- Subscribe called for {} ({})'.format(player, player.lifeform().turn_modifier()))
        if self.active_player is None or (isinstance(player, erukar.engine.model.PlayerNode) and isinstance(self.active_player, erukar.engine.lifeforms.Enemy)):
            self.active_player = player
        self.refresh_deck()
        logger.info('TurnManager -- New Deck is {}'.format(self.on_deck))

    def unsubscribe(self, player):
        super().unsubscribe(player)
        self.refresh_deck()

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
        logger.info('TurnManager -- Refresh Called. Number of players is {}'.format(len(self.players)))
        if len(self.players) < 1: 
            self.reset()
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
