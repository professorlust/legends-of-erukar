from erukar.game.enemies.templates.YoungDragon import YoungDragon
import erukar

class YoungBlackDragon(YoungDragon):
    BaseDamageMitigations = {
        'piercing': (0.10, 0),
        'slashing': (0.35, 0),
        'bludgeoning': (0.20, 0),
        'acid': (1, 0)
    }
    def __init__(self):
        super().__init__("Young Black Dragon")
        self.define_level(11)
        self.spells = [erukar.game.magic.predefined.AcidBreath()]
