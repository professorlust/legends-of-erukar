from erukar.game.enemies.templates.ElderDragon import ElderDragon
import erukar

class ElderBlueDragon(ElderDragon):
    BaseDamageMitigations = {
        'piercing': (0.15, 0),
        'slashing': (0.40, 0),
        'bludgeoning': (0.30, 0),
        'acid': (1, 0)
    }

    def __init__(self, random=True):
        super().__init__("Elder Blue Dragon", random)
        self.define_level(30)
        self.spells = [erukar.game.magic.predefined.IceBreath()]
