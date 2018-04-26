import erukar
from erukar.system.engine import Merchant

class Smithy(Merchant):
    def __init__(self, world):
        super().__init__(world)
        self.desired_item_types = [
            erukar.system.Armor,
            erukar.system.Weapon
        ]

    def interaction_text(self):
        return 'Trade with Smith {}'.format(self.npc.alias())

    def standard_inventory(self):
        return [
            erukar.content.Axe(modifiers=[erukar.content.Iurwood]),
            erukar.content.Axe(modifiers=[erukar.content.Iurwood]),
            erukar.content.Axe(modifiers=[erukar.content.Iurwood]),
            erukar.content.Club(modifiers=[erukar.content.Oak]),
            erukar.content.Dagger(modifiers=[erukar.content.Iron]),
            erukar.content.Dagger(modifiers=[erukar.content.Iron]),
            erukar.content.Dagger(modifiers=[erukar.content.Steel]),
            erukar.content.Dagger(modifiers=[erukar.content.Steel]),
            erukar.content.Longsword(modifiers=[erukar.content.Iron]),
            erukar.content.Longsword(modifiers=[erukar.content.Steel]),
            erukar.content.Longsword(modifiers=[erukar.content.Steel]),
            erukar.content.Mace(modifiers=[erukar.content.Iron]),
            erukar.content.Mace(modifiers=[erukar.content.Iron]),
            erukar.content.Shortbow(modifiers=[erukar.content.Iurwood]),
            erukar.content.Shortbow(modifiers=[erukar.content.Oak]),
            erukar.content.Shortbow(modifiers=[erukar.content.Oak]),
            erukar.content.Brigandine(modifiers=[erukar.content.Leather]),
            erukar.content.Brigandine(modifiers=[erukar.content.Leather]),
            erukar.content.Robes(modifiers=[erukar.content.Cotton]),
            erukar.content.Robes(modifiers=[erukar.content.Cotton]),
            erukar.content.Vest(modifiers=[erukar.content.Leather]),
            erukar.content.Vest(modifiers=[erukar.content.Leather]),
            erukar.content.Boots(modifiers=[erukar.content.Leather]),
            erukar.content.Boots(modifiers=[erukar.content.Leather]),
            erukar.content.Sandals(modifiers=[erukar.content.Leather]),
            erukar.content.Sandals(modifiers=[erukar.content.Leather]),
            erukar.content.Gloves(modifiers=[erukar.content.Leather]),
            erukar.content.Gloves(modifiers=[erukar.content.Leather]),
            erukar.content.Cap(modifiers=[erukar.content.Cotton]),
            erukar.content.Cap(modifiers=[erukar.content.Cotton]),
            erukar.content.Burgonet(modifiers=[erukar.content.Iron]),
            erukar.content.Burgonet(modifiers=[erukar.content.Iron]),
            erukar.content.Leggings(modifiers=[erukar.content.Chainmail]),
            erukar.content.Leggings(modifiers=[erukar.content.Chainmail]),
            erukar.content.Breeches(modifiers=[erukar.content.Leather]),
            erukar.content.Breeches(modifiers=[erukar.content.Leather]),
            erukar.content.Breeches(modifiers=[erukar.content.Cotton]),
            erukar.content.Buckler(modifiers=[erukar.content.Iron]),
            erukar.content.Buckler(modifiers=[erukar.content.Iron]),
            erukar.content.HeaterShield(modifiers=[erukar.content.Steel]),
            erukar.content.HeaterShield(modifiers=[erukar.content.Steel]),
            erukar.content.Torch(),
            erukar.content.Torch(),
            erukar.content.Torch(),
            erukar.content.Torch(),
            erukar.content.Torch(),
            erukar.content.Arrow(50, modifiers=[erukar.content.Atherite]),
            erukar.content.CrossbowBolt(50, modifiers=[erukar.content.Salericite]),
        ]
