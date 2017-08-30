from erukar.system.engine import NpcTemplate
from erukar.content.inventory import *

class Shopkeeper(NpcTemplate):
    def __init__(self):
        super().__init__()

    def get_state(self, npc): 
        return {
            'type': 'Shop',
            'title': '{}\'s Shop'.format(npc.alias()),
            'wealth': npc.wealth,
            'inventory': [self.format_item(x) for x in npc.inventory]
        }

    def format_item(self, item):
        object_output = {
            'id': str(item.uuid),
            'alias': item.alias(),
        }
        return object_output
