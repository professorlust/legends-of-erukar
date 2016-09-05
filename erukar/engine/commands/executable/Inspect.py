from erukar.engine.model.Command import Command
from erukar.engine.model.Containable import Containable

class Inspect(Command):
    not_found = "Nothing matching '{0}' was found in this room."
    abyss = "There is nothing to your {0} except the abyss... plain and nothingness forever."

    aliases = ['look', 'search']

    def __init__(self):
        super().__init__()

    def execute(self):
        player = self.find_player()
        room = player.character.current_room
        self.index(room, player)
        direction = self.determine_direction(self.payload.lower())

        if direction is None:
            return self.inspect_in_room(player, room, self.payload)

        result = room.directional_inspect(direction, player.lifeform())
        if result is None:
            return Inspect.abyss.format(direction.name)
        return result

    def inspect_in_room(self, player, room, payload):
        '''Used if the player didn't specify a direction'''
        if payload in ['','room']:
            return room.inspect_here(player.lifeform())

        if payload in 'flooring':
            return room.floor.on_inspect()

        if payload in 'ceiling':
            return room.ceiling.on_inspect()

        item = self.find_in_room(room, payload)
        if item is not None:
            return self.inspect_item(item, player)

        return Inspect.not_found.format(payload)

    def inspect_item(self, item, player):
        '''Inspect an item and index it if it's a container'''
        self.index(item, player)
        return item.on_inspect(player)

    def index(self, container, player):
        '''Indexes all items in a container for the PlayerNode's indexer'''
        if issubclass(type(container), Containable):
            for i in container.contents:
                player.index_item(i, container)