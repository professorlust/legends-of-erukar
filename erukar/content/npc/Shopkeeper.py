from erukar.system.engine import NpcTemplate
from erukar.content.inventory import *

class Shopkeeper(NpcTemplate):
    def __init__(self):
        super().__init__()

    def get_state(self, npc, for_player): 
        return {
            'type': 'Shop',
            'title': '{}\'s Shop'.format(npc.alias()),
            'wealth': npc.wealth,
            'inventory': list(self.process_inventory(npc, for_player))
        }

    def process_inventory(self, npc, for_player):
        mapped_items = set()
        for item in npc.inventory:
            if item.__module__ in mapped_items: continue
            mapped_items.add(item.__module__)
            quantity = len([x for x in npc.inventory if x.__module__ == item.__module__])
            yield self.format_item(item, for_player, quantity) 


    def format_item(self, item, for_player, quantity):
        object_output = {
            'id': str(item.uuid),
            'alias': item.alias() if quantity <= 1 else '{} x{}'.format(item.alias(), quantity),
            'quantity': quantity,
            'price': item.price(),
        }
        return object_output
