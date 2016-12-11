from erukar.game.enemies.templates.Dragon import Dragon
import erukar

class BlueDragon(Dragon):
    BaseDamageMitigations = {
        'piercing': (0.15, 0),
        'slashing': (0.40, 0),
        'bludgeoning': (0.30, 0),
        'ice': (1, 0)
    }

    def __init__(self):
        super().__init__("Blue Dragon")
        self.define_level(15)
        self.spells = [erukar.game.magic.predefined.IceBreath()]


