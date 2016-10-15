from erukar.game.enemies.templates.YoungDragon import YoungDragon
import erukar

class YoungBlueDragon(YoungDragon):
    BaseDamageMitigations = {
        'piercing': (0.10, 0),
        'slashing': (0.35, 0),
        'bludgeoning': (0.20, 0),
        'ice': (1, 0)
    }

    def __init__(self):
        super().__init__("Young Blue Dragon")
        self.define_level(10)
        self.spells = [erukar.game.magic.predefined.IceBreath()]
