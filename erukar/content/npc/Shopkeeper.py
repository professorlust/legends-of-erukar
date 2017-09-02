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
            'inventory': [self.format_item(x, for_player) for x in npc.inventory]
        }

    def format_item(self, item, for_player):
        object_output = {
            'id': str(item.uuid),
            'alias': item.alias(),
            'price': item.price(),
        }
        return object_output
