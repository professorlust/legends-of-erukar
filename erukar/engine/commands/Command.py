from erukar.engine.model.Direction import Direction
from erukar.engine.commands.CommandResult import CommandResult
import erukar

class Command:
    OverridesUntilSuccess = False

    def __init__(self):
        '''These parameters are assigned after instantiation'''
        self.sender_uid = ''
        self.data = None
        self.context = None
        self.user_specified_payload = ''
        self.arguments = {}
        self.dirtied_characters = []
        self.indexed_items = []
        self.results = {}

    def payload(self):
        if isinstance(self.context, erukar.engine.commands.CommandResult):
            if self.user_specified_payload.isdigit() and int(self.user_specified_payload) in self.context.indexed_items:
                return self.context.indexed_items[int(self.user_specified_payload)]
        return self.user_specified_payload

    def process_arguments(self):
        pass

    def clean(self, lifeform):
        if lifeform in self.dirtied_characters:
            self.dirtied_characters.remove(lifeform)

    def dirty(self, lifeform):
        if lifeform not in self.dirtied_characters:
            self.dirtied_characters.append(lifeform)

    def append_result(self, uid, result):
        '''Appends a result for a specific uid'''
        if uid not in self.results:
            self.results[uid] = []
        self.results[uid].append(result)

    def set_indexed_items(self, items):
        self.indexed_items = items

    def succeed_if_any_results(self, msg_if_failure):
        if len(self.results) > 0:
            return self.succeed()
        return self.fail(msg_if_failure)

    def succeed(self):
        return CommandResult(True, self, self.results, self.indexed_items, self.dirtied_characters)

    def fail(self, result):
        failure_msg = {self.sender_uid: [result]}
        return CommandResult(False, self, failure_msg, self.indexed_items, None)

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
        matches = [p for p in set(container.contents + player.reverse_index(container)) if p.matches(item_name)]
        self.set_indexed_items({i+1: x for i,x in enumerate(matches)})
        return matches

    def lifeform(self, player_or_node):
        if hasattr(player_or_node, 'character'):
            return player_or_node.character
        return player_or_node

    def find_in_inventory(self, player, item_name):
        '''Attempt to find an item in a player's inventory'''
        return next(self.inventory_find(player, item_name), None)

    def find_spell(self, lifeform, spell_name):
        return next(self.spell_find(lifeform, spell_name), None)

    def find_all_in_inventory(self, player, item_name):
        return list(self.inventory_find(player, item_name))

    def inventory_find(self, player, item_name):
        for p in self.lifeform(player).inventory:
            if p.matches(item_name):
                yield p

    def spell_find(self, lifeform, spell_name):
        for p in lifeform.spells:
            if spell_name.lower() in p.name.lower():
                yield p

    def determine_direction(self, text):
        '''Take text and determine its respective cardinal direction'''

        couples = [
            { "keywords": ['n', 'north'], "direction": Direction.North },
            { "keywords": ['e', 'east'], "direction": Direction.East },
            { "keywords": ['s', 'south'], "direction": Direction.South },
            { "keywords": ['w', 'west'], "direction": Direction.West } ]

        return next((x['direction'] for x in couples \
            if any([k == text for k in x['keywords']])), None)
