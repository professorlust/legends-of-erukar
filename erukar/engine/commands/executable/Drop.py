from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.commands.executable.Unequip import Unequip

class Drop(ActionCommand):
    no_item = 'Cannot find {} in inventory.'
    dropped = 'You dropped {} in the current room.'

    aliases = ['drop']

    def execute(self):
        player = self.find_player()
        payload = self.payload()
        room = player.character.current_room

        item = self.find_in_inventory(player, payload)
        if item is None:
            return self.fail(Drop.no_item.format(payload))

        # We have the item, so actually remove it
        self.move_from_inventory(item, player.lifeform(), room)
        drop_result = Drop.dropped.format(item.alias())
        self.append_result(self.sender_uid, drop_result)
        self.succeed()

    def move_from_inventory(self, item, lifeform, room):
        self.try_to_unequip(item.alias())
        lifeform.inventory.remove(item)
        item.on_drop(room,lifeform)
        room.add(item)
        self.dirty(lifeform)

    def try_to_unequip(self, alias):
        u = Unequip()
        u.data = self.data
        u.user_specified_payload = alias
        u.sender_uid = self.sender_uid
        u.execute()
