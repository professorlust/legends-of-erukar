import erukar
from erukar.system.engine import Merchant


class TradeCommissioner(Merchant):
    def __init__(self, world):
        super().__init__(world)
        self.desired_item_types = [
            erukar.system.MaterialGood
        ]

    def interaction_text(self):
        return 'Broker a trade with Commissioner {}'.format(self.npc.alias())

    def standard_inventory(self):
        return []
