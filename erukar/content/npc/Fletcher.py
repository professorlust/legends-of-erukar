import erukar
from erukar.system.engine import Merchant


class Fletcher(Merchant):
    def __init__(self, world):
        super().__init__(world)
        self.desired_item_types = [
            erukar.engine.Ammunition,
            erukar.system.inventory.BowWeapon,
            erukar.system.inventory.CrossbowWeapon,
            erukar.content.inventory.RawWoodMaterial
        ]

    def interaction_text(self):
        return 'Trade with Fletcher {}'.format(self.npc.alias())

    def standard_inventory(self):
        return [
            erukar.content.Shortbow(modifiers=[erukar.content.Iurwood]),
            erukar.content.Shortbow(modifiers=[erukar.content.Iurwood]),
            erukar.content.Shortbow(modifiers=[erukar.content.Ash]),
            erukar.content.Shortbow(modifiers=[erukar.content.Ash]),
            erukar.content.Longbow(modifiers=[erukar.content.Iurwood]),
            erukar.content.Longbow(modifiers=[erukar.content.Iurwood]),
            erukar.content.Longbow(modifiers=[erukar.content.Ash]),
            erukar.content.Longbow(modifiers=[erukar.content.Ash]),
            erukar.content.Arrow(500, modifiers=[erukar.content.Ash]),
            erukar.content.Arrow(500, modifiers=[erukar.content.Iurwood]),
            erukar.content.CrossbowBolt(500, modifiers=[erukar.content.Ash]),
            erukar.content.CrossbowBolt(500, modifiers=[erukar.content.Iurwood]),
        ]
