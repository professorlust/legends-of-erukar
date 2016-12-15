from erukar.engine.lifeforms.Enemy import Enemy

class UndeadKnight(Enemy):
    BriefDescription = "an Undead Knight"
    RandomizedArmor = [
        ('left', 'erukar.game.inventory.armor.shields'),
        ('feet', 'erukar.game.inventory.armor.boots'),
        ('arms', 'erukar.game.inventory.armor.hands'),
        ('legs', 'erukar.game.inventory.armor.pants'),
        ('chest', 'erukar.game.inventory.armor.boots'),
        ('head', 'erukar.game.inventory.armor.helm')
    ]
    RandomizedWeapons = ['right']

    def __init__(self, random=True):
        super().__init__("Undead Knight", random)
        self.str_ratio = 0.2
        self.dex_ratio = 0.2
        self.vit_ratio = 0.1
        self.acu_ratio = 0.1
        self.sen_ratio = 0.1
        self.res_ratio = 0.3
        self.define_level(14)
        self.randomize_equipment()
