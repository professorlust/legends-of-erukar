from erukar.game.enemies.templates.YoungDragon import YoungDragon
import erukar

class YoungYellowDragon(YoungDragon):
    BaseDamageMitigations = {
        'piercing': (0.10, 0),
        'slashing': (0.35, 0),
        'bludgeoning': (0.20, 0),
        'electric': (1, 0)
    }

    def __init__(self):
        super().__init__("Young Yellow Dragon")
        self.define_level(11)
        self.spells = [erukar.game.magic.predefined.ElectricBreath()]
