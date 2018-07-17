from ..Command import Command
from ..auto.Stats import Stats


class AddStatPoint(Command):
    Success = 'Successfully upgraded {} to {}'
    ValidStats = [
        'strength',
        'dexterity',
        'vitality',
        'acuity',
        'sense',
        'resolve'
    ]

    RebuildZonesOnSuccess = True

    def perform(self):
        stat = self.args.get('stat', None)
        if not stat:
            raise Exception('Malformed message received by Add Stat Point')
        if stat.lower() not in AddStatPoint.ValidStats:
            return self.fail('Not a valid stat to upgrade')

        player = self.args['player_lifeform']
        if player.stat_points <= 0:
            return self.fail('You have no stat points to spend!')

        self.dirty(player)
        player.stat_points -= 1
        current_value = getattr(player, stat.lower())
        setattr(player, stat.lower(), current_value + 1)
        self.log(player, self.Success.format(stat, current_value+1))
        payload = {
            'stat': stat,
            'newValue': Stats.format_stat(player, stat)
        }
        self.add_to_outbox(player, 'change stat', payload)
        return self.succeed()
