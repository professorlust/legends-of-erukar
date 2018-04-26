import erukar
from erukar.system.engine import Merchant

class Forester(Merchant):
    def __init__(self, world):
        super().__init__(world)
        self.desired_item_types = [
            erukar.content.RawWoodMaterial,
            erukar.content.AxeWeapon,
            erukar.content.inventory.RawWoodMaterial
        ]

    def interaction_text(self):
        return 'Broker a trade with Forester {}'.format(self.npc.alias())

    def standard_inventory(self):
        return [
            erukar.content.AshLumber(500),
            erukar.content.IurwoodLumber(500),
            erukar.content.Axe(modifiers=[erukar.content.Iurwood]),
            erukar.content.Axe(modifiers=[erukar.content.Iurwood]),
            erukar.content.Axe(modifiers=[erukar.content.Iurwood]),
        ]
