from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Use(ActionCommand):
    unlock = "{} successfully unlocked the {}!"

    aliases = ['use']

    def execute(self):
        player = self.find_player()
        if player is None: return
        payload = self.check_for_arguments()

        # Get the subject
        items = self.find_all_in_inventory(player, payload)
        if len(items) == 0:
            return self.fail('Could not find item "{}".',format(payload))

        # Get the object
        target = None
        if 'object' in self.arguments:
            target = self.determine_target(player)

        for item in items:
            if isinstance(item, erukar.engine.inventory.Key):
                if self.use_key(item, target, self.lifeform(player)):
                    return self.succeed(self.unlock.format(self.lifeform(player).alias(), target.alias()))

        return self.fail('Cannot use anything.')

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
        payload = self.payload()
        if ' on ' in payload:
            args = payload.split(' on ', 1)
            self.arguments['object'] = args[1]
            return args[0]
