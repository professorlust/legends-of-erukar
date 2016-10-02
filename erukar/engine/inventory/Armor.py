from erukar.engine.inventory.Item import Item

class Armor(Item):
    EquipmentLocations = ['chest']
    Persistent = True
    EssentialPart = "armor"
    DexPenalty = 2
    DamageMitigations = [
        # type, mitigation percent, glancing range
        ('bludgeoning', 0.05, 2),
        ('piercing', 0.1, 4)
    ]

    def __init__(self, name="Armor"):
        super().__init__("armor", name)

    def on_inventory(self):
        equip_loc = ', '.join(x.capitalize() for x in self.EquipmentLocations)
        return '{} [{}] ({}%)'.format(self.name, equip_loc, int(100*self.durability/self.MaxDurability))

    def on_inventory_inspect(self):
        name = '{} ({} / {})'.format(self.name, self.durability, self.MaxDurability)
        mit_desc = '\n'.join(['\t\t  {}: {}% MIT / {} DFL'.format(x[0].capitalize(), x[1]*100.0, x[2]) for x in self.DamageMitigations])
        mods = [self.material] + self.modifiers if self.material else self.modifiers
        mod_desc = '\n'.join(['\t\t• {}'.format(d.mutate(d.InventoryDescription)) for d in mods])
        return '\n'.join([name, mit_desc, mod_desc])

