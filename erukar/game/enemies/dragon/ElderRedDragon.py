from erukar.game.enemies.templates.ElderDragon import ElderDragon
import erukar

class ElderRedDragon(ElderDragon):
    BaseDamageMitigations = {
        'piercing': (0.15, 0),
        'slashing': (0.40, 0),
        'bludgeoning': (0.30, 0),
        'acid': (1, 0)
    }

    def __init__(self):
        super().__init__("Elder Red Dragon")
        self.define_level(32)
        self.spells = [erukar.game.magic.predefined.AcidBreath()]
