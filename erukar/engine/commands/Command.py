from erukar.engine.model.Direction import Direction
from erukar.engine.commands.CommandResult import CommandResult
import erukar

class Command:
    OverridesUntilSuccess = False
    not_found = "No object matching '{}' was found in this room."
    MultipleOptions = "Multiple matches for '{}' were found, please specify with a number between 1 and {}.\n\n{}"
    TrackedParameters = []

    def __init__(self):
        '''These parameters are assigned after instantiation'''
        self.sender_uid = ''
        self.data = None
        self.context = None
        self.user_specified_payload = ''
        self.arguments = {}
        self.dirtied_characters = []
        self.indexed_items = {}
        self.results = {}

    def check_for_arguments(self):
        # Copy alreturol of the tracked Params into this command
        payload = self.user_specified_payload
        self.player = self.find_player()
        self.lifeform = self.player.lifeform()
        self.room = self.lifeform.current_room

        if self.context and self.context.requires_disambiguation and payload.isdigit():
            self.context.resolve_disambiguation(self.context.indexed_items[int(payload)])

        for param_name in self.TrackedParameters:
            method_name = 'resolve_{}'.format(param_name)
            actual_method = getattr(self, method_name)
            failed = actual_method(payload)
            if failed: return failed

        # Check to make sure all tracked parameters are set
        return self.fail_if_requires_disambiguation()

    def process_input_payload(self, payload):
        '''Processes an input string and sets variables accordingly'''
        return

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

    def add_items_to_context(self, items):
        pre_insertion_length = len(self.indexed_items)+1
        for index, alias in enumerate(items):
            self.indexed_items[pre_insertion_length + index] = items[alias]

    def succeed_if_any_results(self, msg_if_failure):
        if len(self.results) > 0:
            return self.succeed()
        return self.fail(msg_if_failure)

    def succeed(self):
        result = CommandResult(True, self, self.results, self.indexed_items, self.dirtied_characters)
        self.sever()
        return result

    def fail(self, result):
        failure_msg = {self.sender_uid: [result]}
        result = CommandResult(False, self, failure_msg, self.indexed_items, None)
        self.sever()
        return result

    def sever(self):
        self.indexed_items = None
        self.results = None
        self.data = None
        self.arguments = None
        self.context = None

    def execute(self):
        '''Run this Command as a player'''
        player = self.find_player()

    def find_player(self):
        '''Attempt to find a player in the data access component'''
        return self.data.find_player(self.sender_uid)

    def find_in_target(self, payload, target, for_field_name, additionals=None):
        '''Attempts to find something matching a payload in a super set of
        target.contents, additionals, and self.player.reverse_index(target)'''
        player = self.find_player()
        full_map = additionals if additionals else {}
        target_contents_map = {x.alias(): x for x in set(target.contents + player.reverse_index(target))}
        full_map.update(target_contents_map)
        matches = {alias: full_map[alias] for alias in full_map if self.any_matches(alias, payload)}
        return self.post_process_search(matches, payload, for_field_name)

    def any_matches(self, alias, payload):
        return any(alias_substr.lower().startswith(payload.lower()) for alias_substr in alias.split())

    def find_in_dictionary(self, payload, dictionary, for_field_name):
        matches = {alias: dictionary[alias] for alias in dictionary if self.any_matches(alias, payload)}
        return self.post_process_search(matches, payload, for_field_name)
        
    def post_process_search(self, matches, payload, field_name):
        '''
        Handles edge cases on searching, sets indexed items for contextual  results.
        If there are 0 results, it fails the command out. If there are >1 results, it fails
        and requests further clarification. If there are exactly 1 results, it returns
        that as the target.

        Output: direct_match_if_not_failure, failure_object
        '''
        self.add_items_to_context(matches)
        if len(matches) == 0:
            return self.fail(self.not_found.format(payload))

        # If there's more than one, we must ask for clarification
        if len(matches) > 1:
            match_list = self.enumerate_options(matches)
            failure = self.fail(self.MultipleOptions.format(payload, len(matches), match_list))
            failure.disambiguating_parameter = field_name
            failure.requires_disambiguation = True
            return failure

        setattr(self, field_name, next(iter(matches.values())))

    def enumerate_options(self, targets):
        return '\n'.join(['{:3}. {}'.format(i+1, self.readable(x)) for i,x in enumerate(targets)])

    def readable(self, x):
        if hasattr(x, 'alias'):
            return x.alias()
        return x

    def lifeform(self, player_or_node):
        if hasattr(player_or_node, 'character'):
            return player_or_node.character
        return player_or_node

    def find_in_inventory(self, player, item_name, field_name):
        '''Attempt to find an item in a player's inventory'''
        inventory_list = {item.alias(): item for item in player.inventory}
        print(inventory_list)
        return self.find_in_dictionary(item_name, inventory_list, field_name)

    def find_spell(self, player, payload, field_name):
        spell_book = {spell.alias(): spell for spell in player.spells} 
        return self.find_in_dictionary(payload, spell_book, field_name)

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

    def fail_if_requires_disambiguation(self):
        for tracked in self.TrackedParameters:
            tracked_val = getattr(self, tracked, None)
            if not tracked_val:
                failure = self.fail('Missing parameter {}'.format(tracked))
                failure.disambiguating_parameter = tracked
                failure.requires_disambiguation = True
                return failure

    def resolve_direction(self, opt_payload=''):
        '''If we're tracking direction, it should default here'''
        # If this is on the context, grab it and return
        if self.context and self.context.should_resolve(self):
            self.direction = getattr(self.context, 'direction')

        # If we have the parameter and it's not nully, assert that we're done
        if hasattr(self, 'direction') and self.direction: return
        directions = {
            'North': Direction.North,
            'East': Direction.East,
            'South': Direction.South,
            'West': Direction.West
        }

        return self.find_in_dictionary(opt_payload, directions, 'direction')

    def resolve_target(self, opt_payload=''):
        # If this is on the context, grab it and return
        if self.context and self.context.should_resolve(self):
            self.target = getattr(self.context, 'target')

        # If we have the parameter and it's not nully, assert that we're done
        if hasattr(self, 'target') and self.target: return

        direction = self.determine_direction(opt_payload.lower())
        if direction:
            self.target = direction
            return

        if opt_payload == 'self':
            self.target = self.player.lifeform()
            return

        failure_object = self.find_in_target(opt_payload, self.room, 'target')
        return failure_object

    def resolve_item(self, opt_payload=''):
        # If this is on the context, grab it and return
        if self.context and self.context.should_resolve(self):
            self.item = getattr(self.context, 'item')

        # If we have the parameter and it's not nully, assert that we're done
        if hasattr(self, 'item') and self.item: return

        # Start looking at the payload for the item
        return self.find_in_inventory(self.lifeform, opt_payload, 'item')
