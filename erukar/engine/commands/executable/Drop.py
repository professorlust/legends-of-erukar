from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.commands.executable.Unequip import Unequip

class Drop(ActionCommand):
    no_item = 'Cannot find {} in inventory.'
    dropped = 'You dropped {} in the current room.'

    aliases = ['drop']
    TrackedParameters = ['item']

    def execute(self):
        failure = self.check_for_arguments()
        if failure: return failure

        # We have the item, so actually remove it
        self.move_from_inventory()
        drop_result = Drop.dropped.format(self.item.alias())
        self.append_result(self.sender_uid, drop_result)
        self.succeed()

    def move_from_inventory(self):
        self.try_to_unequip()
        self.lifeform.inventory.remove(self.item)
        self.item.on_drop(self.room, self.lifeform)
        self.room.add(self.item)
        self.dirty(self.lifeform)

    def try_to_unequip(self):
        u = Unequip()
        u.data = self.data
        u.user_specified_payload = self.item.alias()
        u.sender_uid = self.sender_uid
        u.execute()
