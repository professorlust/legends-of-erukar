from erukar.game.enemies.templates.Dragon import Dragon
import erukar

class BlackDragon(Dragon):
    BaseDamageMitigations = {
        'piercing': (0.15, 0),
        'slashing': (0.40, 0),
        'bludgeoning': (0.30, 0),
        'acid': (1, 0)
    }

    def __init__(self, random=True):
        super().__init__("Black Dragon", random)
        self.define_level(16)
        self.spells = [erukar.game.magic.predefined.AcidBreath()]
