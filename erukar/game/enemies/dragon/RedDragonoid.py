from erukar.game.enemies.templates.Dragonoid import Dragonoid
import random

class RedDragonoid(Dragonoid):
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
        'fire': (0.4, 0)
    }

    def __init__(self):
        super().__init__("Red Dragonoid")
