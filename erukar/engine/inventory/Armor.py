from erukar.engine.inventory.Item import Item
from erukar.engine.model.Damage import Damage

class Armor(Item):
    EquipmentLocations = ['chest']
    Persistent = True
    EssentialPart = "armor"
    DamageMitigations = {
        # type, mitigation percent, glancing range
        'bludgeoning': (0.05, 2),
        'piercing': (0.1, 4)
    }

    def __init__(self, name="Armor",modifiers=None):
        super().__init__("armor", name, modifiers=modifiers)

    def on_inventory(self):
        '''Basic inventory description; includes information about possible equipment locations and durability'''
        equip_loc = ', '.join(x.capitalize() for x in self.EquipmentLocations)
        return '{} [{}] ({}%)'.format(self.format(), equip_loc, int(100*self.durability_coefficient))

    def on_inventory_inspect(self, lifeform):
        '''This is what you get whenever you inspect something in your inventory, or whenever you view your equipped items'''
        name = '{} ({} / {})'.format(self.format(), int(self.durability()), int(self.max_durability()))
        mit_desc = '\n'.join(list(self.mitigation_descriptions()))
        mods = [self.material] + self.modifiers if self.material else self.modifiers
        mod_desc = '\n'.join(['{:>11} {:12}: {}'.format('+', d.InventoryName, d.mutate(d.InventoryDescription)) for d in mods])
        weight_desc = '{:>11} {:12}: {:3.2} levts'.format('+', 'Weight:', self.weight())
        inv_desc = '{:>11} {}'.format('+', self.InventoryDescription)
        return '\n'.join([name, weight_desc, mit_desc, mod_desc, inv_desc])

    def mitigation_for(self, damage_type):
        '''result is (%MIT, DFL)'''
        if self.durability_coefficient > 0.0 and damage_type in self.DamageMitigations:
            mat_mult = self.material.mitigation_multiplier_for(damage_type)
            return (
                self.DamageMitigations[damage_type][0] * mat_mult[0],
                int(self.DamageMitigations[damage_type][1] * mat_mult[1]),
            )
        return (0, 0)

    def mitigation_descriptions(self, show_non_empty=False):
        for dam_type in Damage.Types:
            if dam_type in self.DamageMitigations or show_non_empty:
                mit, dfl = self.mitigation_for(dam_type)
                if mit > 0 and dfl > 0:
                    yield '{:>11} {:12}: {:3.0f}% MIT / {:3} DFL'.format('-',dam_type.capitalize(), mit*100.0, dfl)

