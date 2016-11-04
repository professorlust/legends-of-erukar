from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.model.Containable import Containable
import random, math, erukar

class Inspect(ActionCommand):
    not_found = "Nothing matching '{0}' was found in this room."
    abyss = "There is nothing to your {0} except the abyss... plain and nothingness forever."

    aliases = ['inspect', 'look', 'search']

    def __init__(self):
        super().__init__()

    def execute(self):
        player = self.find_player()
        room = player.lifeform().current_room

        self.acuity, self.sense = [math.floor(random.uniform(*player.lifeform().stat_random_range(x))) for x in ('acuity', 'sense')]

        # Index in the player's active indexing tree
        self.index(room, player)
        payload, target = self.check_for_arguments()
        if target:
            self.add_items_to_context(self.context.indexed_items.values())
            result = self.inspect_item(target, player)
            self.append_result(self.sender_uid, result)
            return self.succeed()

        direction = self.determine_direction(payload.lower())
        if direction:
            result = room.directional_inspect(direction, player.lifeform())
            self.append_result(self.sender_uid, result)
            return self.succeed()

        return self.inspect_in_room(player, room, payload)

    def inspect_in_room(self, player, room, payload):
        '''Used if the player didn't specify a direction'''
        lifeform = player.lifeform()
        result = ''

        if payload == 'room':
            result = room.on_inspect(lifeform, self.acuity, self.sense)

        if payload == 'flooring':
            result = room.floor.on_inspect(lifeform, self.acuity, self.sense)

        if payload == 'ceiling':
            result = room.ceiling.on_inspect(lifeform, self.acuity, self.sense)

        if not result:
            item, failure_object = self.find_in_room(room, payload)
            if failure_object:
                return failure_object
            result = self.inspect_item(item, player)

        self.append_result(self.sender_uid, result)
        return self.succeed()

    def inspect_item(self, item, player):
        '''Inspect an item and index it if it's a container'''
        self.index(item, player)
        return item.on_inspect(player, self.acuity, self.sense)

    def index(self, container, player):
        '''Indexes all items in a container for the PlayerNode's indexer'''
        if issubclass(type(container), Containable):
            for i in container.contents:
                player.index_item(i, container)
