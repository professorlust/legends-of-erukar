from erukar.system.engine import Merchant

class Shopkeeper(Merchant):
    def interaction_text(self):
        return 'Browse {}\'s Shop'.format(self.npc.alias())

    def standard_inventory(self):
        return []
