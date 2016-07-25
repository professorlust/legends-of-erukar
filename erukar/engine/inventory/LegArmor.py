from erukar.engine.inventory.Armor import Armor

class LegArmor(Armor):
    '''Basic LegArmor; shouldn't appear in game, but if it does that's okay'''
    def __init__(self, name):
        super().__init__(name)
        self.equipment_locations = ['legs']
        self.armor_class_modifier = 1
        self.max_dex_mod = 5

    def on_inventory(self, *_):
       return '{}\n\t+{} AC\n\tMax {} Dex Mod'.format(self.alias(), self.armor_class_modifier, self.max_dex_mod)
