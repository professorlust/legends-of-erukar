class Lifeform:
    def __init__(self):
        self.attributes = {}
        self.armor = None
        self.weapon = None
        self.level = 0
        self.health = 0

    def define_stats(self, strength=-2, dexterity=-2, vitality=-2):
        self.attributes = { 'str': strength, 'dex': dexterity, 'vit': vitality }

    def define_level(self, level):
        self.level = level
        self.health = sum([4+self.attributes['vit'] for x in range(0, level)])
