from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.commands.executable.Unequip import Unequip

class Drop(ActionCommand):
    no_item = 'Cannot find {} in inventory.'
    dropped = 'You dropped {} in the current room.'

    def execute(self):
        player = self.find_player()
        room = player.character.current_room

        item = self.find_in_inventory(player, self.payload)
        if item is None:
            return self.fail(Drop.no_item.format(self.payload))

        self.move_from_inventory(item, player, room)
        return self.succeed(Drop.dropped.format(item.alias()))

    def move_from_inventory(self, item, player, room):
        self.try_to_unequip()
        player.lifeform().inventory.remove(item)
        room.add(item)

    def try_to_unequip(self):
        u = Unequip()
        u.data = self.data
        u.payload = self.payload
        u.sender_uid = self.sender_uid
        u.execute()