from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Use(ActionCommand):
    unlock = "{} successfully unlocked the {}!"

    def execute(self):
        player = self.find_player()
        if player is None: return
        self.check_for_arguments()

        # Get the subject
        items = self.find_all_in_inventory(player, self.payload)
        if len(items) == 0:
            return 'Could not find item "{}".',format(self.payload)

        # Get the object
        target = None
        if 'object' in self.arguments:
            target = self.determine_target(player)

        for item in items:
            if isinstance(item, erukar.engine.inventory.Key):
                if self.use_key(item, target, self.lifeform(player)):
                    return self.unlock.format(self.lifeform(player).alias(), target.alias())

        return 'Cannot use anything.'

    def determine_target(self, player):
        '''Attempts to determine what the target is'''
        direction = self.determine_direction(self.arguments['object'])
        if direction is not None:
            in_direction = self.lifeform(player).current_room.get_in_direction(direction)
            if hasattr(in_direction.door, 'lock'):
                return in_direction.door.lock

        return self.find_in_room(self.arguments['object'])


    def use_key(self, item, target, player):
        if target is None:
            return False

        return item.toggle_lock(target)

    def check_for_arguments(self):
        if ' on ' in self.payload:
            args = self.payload.split(' on ', 1)
            self.payload = args[0]
            self.arguments['object'] = args[1]
