from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Use(ActionCommand):

    def execute(self):
        player = self.find_player()
        if player is None: return
        self.check_for_arguments()

        # Get the subject
        item = self.find_in_inventory(player, self.payload)
        if item is None:
            return 'Could not find item "{}".',format(self.payload)

        # Get the object
        if 'object' in self.arguments:
            direction = self.determine_direction(self.arguments['object'])
            if direction is not None:
                in_direction = self.lifeform(player).current_room.get_in_direction(direction)
                if hasattr(in_direction.door, 'lock'):
                    target = in_direction.door.lock

            if target is None:
                target = self.find_in_room(self.arguments['object'])

        if isinstance(item, erukar.engine.inventory.Key):
            return self.use_key(item, target, player)

        return 'Cannot use anything.'

    def use_key(self, item, target, player):
        if target is None:
            return 'Keys are useless on their own.'

        if item.toggle_lock(target):
            return '{} was successful in unlocking.'.format(player.alias())
        return 'This is not the right key.'


    def check_for_arguments(self):
        if ' on ' in self.payload:
            args = self.payload.split(' on ', 1)
            self.payload = args[0]
            self.arguments['object'] = args[1]
