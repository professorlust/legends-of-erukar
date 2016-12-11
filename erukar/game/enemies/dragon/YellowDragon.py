from erukar.game.enemies.templates.Dragon import Dragon
import erukar

class YellowDragon(Dragon):
    BaseDamageMitigations = {
        'piercing': (0.15, 0),
        'slashing': (0.40, 0),
        'bludgeoning': (0.30, 0),
        'electric': (1, 0)
    }

    def __init__(self):
        super().__init__("Yellow Dragon")
        self.define_level(16)
        self.spells = [erukar.game.magic.predefined.ElectricBreath()]


