from erukar.engine.lifeforms.Enemy import Enemy

class Revenant(Enemy):
    BriefDescription = "a Revenant"
    RandomizedArmor = [
        ('feet', 'erukar.game.inventory.armor.boots'),
        ('arms', 'erukar.game.inventory.armor.hands'),
        ('legs', 'erukar.game.inventory.armor.pants'),
        ('chest', 'erukar.game.inventory.armor.boots'),
    ]
    RandomizedWeapons = ['right', 'left']

    def __init__(self, random=True):
        super().__init__("Revenant", random)
        self.str_ratio = 0.2
        self.dex_ratio = 0.2
        self.vit_ratio = 0.15
        self.acu_ratio = 0.15
        self.sen_ratio = 0.15
        self.res_ratio = 0.15
        self.define_level(10)
        self.randomize_equipment()

