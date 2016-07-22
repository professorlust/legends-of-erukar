from erukar.engine.inventory.Armor import Armor

class Shield(Armor):
    '''Basic Shield; shouldn't appear in game, but if it does that's okay'''
    def __init__(self, name):
        super().__init__(name)
        self.equipment_locations = ['left','right']
        self.armor_class_modifier = 1
        self.max_dex_mod = 5
