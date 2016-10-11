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
        target = player.lifeform()
        if 'object' in self.arguments:
            target = self.determine_target(player)

        for item in items:
            successful = item.on_use(self, target)
            if successful:
                self.dirty(player.lifeform())
                self.dirty(target)
                return self.succeed()

        return self.fail('Cannot use anything.')

    def determine_target(self, player):
        '''Attempts to determine what the target is'''
        direction = self.determine_direction(self.arguments['object'])
        if direction is not None:
            in_direction = self.lifeform(player).current_room.get_in_direction(direction)
            if hasattr(in_direction.door, 'lock'):
                return in_direction.door.lock

        return self.find_in_room(self.arguments['object'])

    def check_for_arguments(self):
        payload = self.payload()
        if ' on ' in payload:
            args = payload.split(' on ', 1)
            self.arguments['object'] = args[1]
            return args[0]
        return payload
