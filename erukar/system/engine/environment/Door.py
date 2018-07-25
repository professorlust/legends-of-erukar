from erukar.system.engine import ErukarActor
import erukar


class Door(ErukarActor):
    close_success = 'You have successfully closed the door'
    open_success = 'You have successfully opened the door'
    already_closed = 'The door is already closed'
    open_success = 'You have successfully opened the door'
    is_locked = 'You try to open the door, but it is locked'
    already_open = 'The door is already open'
    OnUnlock = 'You use a {} to unlock the {}.'
    ViewUnlock = 'You see {} use a {} to unlock the {}.'
    Closed = 'closed'
    Open = 'open'
    generic_description = 'There is a door to the {direction}. It is {status}.'

    def __init__(self):
        super().__init__()
        self.is_open = False
        self.lock_type = None
        self.can_open_or_close = True

    def tile_id(self, is_open=None):
        if is_open is None:
            is_open = self.is_open
        return '{}-{}'.format(str(self.uuid), 'o' if is_open else 'c')

    def ids_to_generate(self):
        return [self.tile_id(is_open=False), self.tile_id(is_open=True)]

    def generate_tile(self, dimensions, tile_id):
        h, w = dimensions
        for y in range(h):
            for x in range(w):
                if (x is 2 or x is w-2) or (y is 2 or y is h-2):
                    yield {'r':205,'g':133,'b':63,'a':1}
                elif 2 < x < (w-2) and 2 < y < (h-2) and tile_id == self.tile_id(is_open=False):
                    yield {'r':139,'g':69,'b':19,'a':1}
                else: yield {'r':0,'g':0,'b':0,'a':0}

    def alias(self):
        return 'door'

    def can_close(self):
        return self.can_open_or_close and self.is_open

    def can_open(self):
        return self.can_open_or_close\
                and not self.is_open\
                and self.lock_type is None

    def actions(self, player):
        if self.is_open:
            yield self.action('close')
        if self.lock_type and player.get_key(self.lock_type):
            yield self.action('unlock')
        if not self.is_open and not self.lock_type:
            yield self.action('open')

    def on_unlock(self, cmd):
        player = cmd.args['player_lifeform']
        key = player.get_key(self.lock_type)
        if not key:
            return cmd.fail('No appropriate key type found!')
        self.remove_key(cmd, key, player)
        cmd.log(player, self.OnUnlock.format(key.alias(), self.alias()))
        cmd.obs(
            self.coordinates,
            self.ViewUnlock.format(player.alias(), key.alias(), self.alias()),
            exclude=[player]
        )
        return cmd.succeed()

    def remove_key(self, cmd, key, player):
        self.lock_type = None
        key.consume()
        payload = {'uid': str(key.uuid)}
        cmd.add_to_outbox(player, 'remove item', payload)

    def action(self, a_type):
        return {
            'command': 'BasicInteraction',
            'description': '{} {}'.format(a_type.capitalize(), self.alias()),
            'cost': 1,
            'interaction_target': str(self.uuid),
            'interaction_type': a_type
        }

    def on_close(self, cmd):
        player = cmd.args['player_lifeform']
        if self.can_close():
            self.is_open = False
            cmd.append_result(player.uid, Door.close_success)
            for aura in cmd.world.get_applicable_auras(self.coordinates):
                aura.needs_rebuilt = True
            return cmd.succeed()
        return cmd.fail("Cannot close this door")

    def on_open(self, cmd):
        player = cmd.args['player_lifeform']
        if self.can_open():
            self.is_open = True
            cmd.append_result(player.uid, Door.open_success)
            for aura in cmd.world.get_applicable_auras(self.coordinates):
                aura.needs_rebuilt = True
            player.observe()
            return cmd.succeed()
        return cmd.fail("Cannot open this door")

    def can_unlock(self, player):
        return not self.is_open \
                and self.lock_type \
                and player.get_key(self.lock_type)
