from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.Rapier import Rapier

class Terrormind(Enemy):
    critical_health = [
        'Terrormind is bleeding profusely and barely holding himself up.']

    badly_wounded = [
        'Terrormind has sustained serious injuries and is badly wounded.']

    wounded = [
        'Terrormind has a few cuts and bruises, but none so bad that he has broken his battle stance.' ]

    slightly_wounded = [
        'The dark-robed Terrormind winces in pain, but shows no injury.' ]

    full_health = [
        'A man in black robes, Terrormind, towers above you in this room.']

    def __init__(self):
        super().__init__("Terrormind")
        self.dexterity = 3
        self.strength = 4
        self.vitality = 2
        self.weapon = Rapier()
        self.name = "Terrormind"
