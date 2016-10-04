from erukar.engine.inventory.Item import Item
from erukar.engine.model.Damage import Damage

class Armor(Item):
    EquipmentLocations = ['chest']
    Persistent = True
    EssentialPart = "armor"
    DexPenalty = 2
    DamageMitigations = {
        # type, mitigation percent, glancing range
        'bludgeoning': (0.05, 2),
        'piercing': (0.1, 4)
    }

    def __init__(self, name="Armor"):
        super().__init__("armor", name)

    def on_inventory(self):
        equip_loc = ', '.join(x.capitalize() for x in self.EquipmentLocations)
        return '{} [{}] ({}%)'.format(self.name, equip_loc, int(100*self.durability/self.MaxDurability))

    def on_inventory_inspect(self):
        name = '{} ({} / {})'.format(self.name, self.durability, self.MaxDurability)
        mit_desc = '\t' + '\n\t'.join(list(self.mitigation_descriptions()))
        mods = [self.material] + self.modifiers if self.material else self.modifiers
        mod_desc = '\n'.join(['\t\t• {}: {}'.format(d.InventoryName, d.mutate(d.InventoryDescription)) for d in mods])
        return '\n'.join([name, mit_desc, mod_desc])

    def mitigation_for(self, damage_type):
        '''result is (%MIT, DFL)'''
        if self.durability > 0 and damage_type in self.DamageMitigations:
            return self.DamageMitigations[damage_type]
        return (0, 0)

    def mitigation_descriptions(self, show_non_empty=False):
        for dam_type in Damage.Types:
            if dam_type in self.DamageMitigations or show_non_empty:
                mit, dfl = self.mitigation_for(dam_type)
                yield '\t  {}: {}% MIT / {} DFL'.format(dam_type.capitalize(), mit*100.0, dfl)

