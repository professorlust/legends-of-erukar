from erukar.engine.model.Direction import Direction

class Command:
    def __init__(self):
        '''These parameters are assigned after instantiation'''
        self.sender_uid = ''
        self.data = None
        self.payload = ''
        self.arguments = {}

    def process_arguments(self):
        pass

    def execute(self):
        '''Run this Command as a player'''
        player = self.find_player()

    def find_player(self):
        '''Attempt to find a player in the data access component'''
        return self.data.find_player(self.sender_uid)

    def find_in_room(self, container, item_name):
        '''Attempt to find an item in a room's contents'''
        player = self.find_player()
        lifeform = self.lifeform(player)
        acuity, sense = (lifeform.calculate_stat_score(x) for x in ['acuity', 'sense'])
        contents = set(container.get_visible_contents(acuity)\
                       + container.get_sensed_contents(sense)\
                       + player.reverse_index(container))
        return next((p for p in contents if p.matches(item_name)), None)

    def lifeform(self, player_or_node):
        if hasattr(player_or_node, 'character'):
            return player_or_node.character
        return player_or_node

    def find_in_inventory(self, player, item_name):
        '''Attempt to find an item in a player's inventory'''
        return next(self.inventory_find(player, item_name), None)

    def find_all_in_inventory(self, player, item_name):
        return list(self.inventory_find(player, item_name))

    def inventory_find(self, player, item_name):
        for p in self.lifeform(player).inventory:
            if p.matches(item_name):
                yield p

    def determine_direction(self, payload):
        '''Take text and determine its respective cardinal direction'''

        couples = [
            { "keywords": ['n', 'north'], "direction": Direction.North },
            { "keywords": ['e', 'east'], "direction": Direction.East },
            { "keywords": ['s', 'south'], "direction": Direction.South },
            { "keywords": ['w', 'west'], "direction": Direction.West } ]

        return next((x['direction'] for x in couples \
            if any([k == payload for k in x['keywords']])), None)
