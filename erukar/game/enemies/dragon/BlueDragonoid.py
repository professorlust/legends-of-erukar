from erukar.game.enemies.templates.Dragonoid import Dragonoid
import random

class BlueDragonoid(Dragonoid):
    RandomizedArmor = [
        ('feet', 'erukar.game.inventory.armor.chest'),
        ('chest', 'erukar.game.inventory.armor.boots'),
        ('head', 'erukar.game.inventory.armor.helm')
    ]
    RandomizedWeapons = [ 'left', 'right' ]
    BaseDamageMitigations = {
        'piercing': (0.05, 0),
        'slashing': (0.10, 0),
        'bludgeoning': (0.15, 0),
        'ice': (0.4, 0)
    }

    def __init__(self, random=True):
        super().__init__("Blue Dragonoid", random)
