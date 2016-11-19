from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Item import Item

class Take(ActionCommand):
    failure = "No item '{0}' was found"
    cannot_take = "'{0}' cannot be taken."
    success = "Successfully took {0}"

    aliases = ['take', 'get', 'grab']
    TrackedParameters = ['target']

    def execute(self):
        failure = self.check_for_arguments()
        if failure: return failure

        self.append_result(self.sender_uid, self.move_to_inventory())
        return self.succeed()

    def move_to_inventory(self):
        if not issubclass(type(self.target), Item):
            return Take.cannot_take.format(self.target.alias().capitalize())

        # We found it, so give it to the player and return a success msg
        self.lifeform.inventory.append(self.target)
        container = self.player.index(self.target)
        self.player.remove_index(self.target)
        if len(container) > 0:
            container[-1].remove(self.target)
        self.target.on_take(self.lifeform)
        self.dirty(self.lifeform)
        return Take.success.format(self.target.describe())
