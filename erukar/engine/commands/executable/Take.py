from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Item import Item

class Take(ActionCommand):
    failure = "No item '{0}' was found"
    cannot_take = "'{0}' cannot be taken."
    success = "Successfully took {0}"

    aliases = ['take', 'get', 'grab']

    def execute(self):
        player = self.find_player()
        if player is None: return

        payload, target = self.check_for_arguments()
        room = player.character.current_room

        if not target:
            # Try to find the item in the room
            target, failure_object = self.find_in_room(room, payload)
            if failure_object:
                return failure_object

        self.append_result(self.sender_uid, self.move_to_inventory(target, player, room))
        return self.succeed()

        # Send a failure message
        return self.fail(Take.failure.format(payload))

    def move_to_inventory(self, item, player, room):
        if not issubclass(type(item), Item):
            return Take.cannot_take.format(item.alias().capitalize())

        # We found it, so give it to the player and return a success msg
        player.lifeform().inventory.append(item)
        container = player.index(item)
        player.remove_index(item)
        if len(container) > 0:
            container[-1].remove(item)
        item.on_take(player.lifeform())
        self.dirty(player.lifeform())
        return Take.success.format(item.describe())
