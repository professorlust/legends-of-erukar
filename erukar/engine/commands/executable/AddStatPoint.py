from erukar.engine.commands.Command import Command
import erukar

class AddStatPoint(Command):
    ValidStats = [
        'strength',
        'dexterity',
        'vitality',
        'acuity',
        'sense',
        'resolve'
    ]

    def perform(self):
        if 'stat' not in self.args: raise Exception('Malformed message received by Add Stat Point')
        print(self.args['stat'])
        if self.args['stat'].lower() not in AddStatPoint.ValidStats:
            return self.fail('Not a valid stat to upgrade')

        if self.args['player_lifeform'].stat_points <= 0:
            return self.fail('You have no stat points to spend!')

        self.dirty(self.args['player_lifeform'])
        self.args['player_lifeform'].stat_points -= 1
        current_value = getattr(self.args['player_lifeform'], self.args['stat'].lower())
        setattr(self.args['player_lifeform'], self.args['stat'].lower(), current_value + 1)
        self.append_result(self.player_info.uid, 'Successfully upgraded {} to {}'.format(self.args['stat'], current_value+1))
        return self.succeed()
