from ..templates.YoungDragon import YoungDragon

class YoungRedDragon(YoungDragon):
    BaseDamageMitigations = {
        'piercing': (0.10, 0),
        'slashing': (0.35, 0),
        'bludgeoning': (0.20, 0),
        'fire': (1, 0)
    }
    def __init__(self, random=True):
        super().__init__("Young Red Dragon", random)
        self.define_level(10)
