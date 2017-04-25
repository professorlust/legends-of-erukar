from erukar.engine.model.RpgEntity import RpgEntity 

class Door(RpgEntity):
    close_success = 'You have successfully closed the door'
    open_success = 'You have successfully opened the door'
    already_closed = 'The door is already closed'
    open_success = 'You have successfully opened the door'
    is_locked = 'You try to open the door, but it is locked'
    already_open = 'The door is already open'
    Closed = 'closed'
    Open = 'open'
    generic_description = 'There is a door to the {direction}. It is {status}.'

    def __init__(self, description=""):
        super().__init__()
        self.lock = None
        self.status = Door.Closed
        self.can_close = True
        self.description = description
        self.acuity_needed = 0
        if self.description is '':
            self.description = self.generic_description

    def on_hear(self, sound, decay=1.0, instigator=None, direction=None):
        if self.lock is not None:
            return self.lock.on_hear(sound,decay,instigator,direction)

    def alias(self):
        return 'door'

    def on_inspect(self, direction):
        return self.mutate(self.description, {'direction': direction.name})

    def on_glance(self, player):
        return 'Glanced at a door: {} ACU, {} SEN'.format(player.acuity, player.sense), True

    def peek(self, direction, room, lifeform, acu, sen):
        '''Does a single look through'''
        if self.status is Door.Open and room is not None:
            return ' '.join([self.on_inspect(direction), room.peek(lifeform, acu, sen)])
        return self.on_inspect(direction)

    def necessary_acuity(self):
        return self.acuity_needed

    def inspect_through(self, direction, room, lifeform, depth):
        '''Allows a directional inspect to continue'''
        if self.status is Door.Open:
            return self.on_inspect(direction) + ' ' + room.directional_inspect(direction, lifeform, depth)
        return self.on_inspect(direction)

    def describe_locked(self):
        if self.lock is None:
            return ''
        return self.lock.describe()

    def describe_lock(self, direction=None):
        if self.lock is not None:
            return self.mutate(self.lock.description)
        return ''

    def on_close(self, player):
        if self.can_close:
            if self.status == Door.Open:
                self.status = Door.Closed
                return Door.close_success, True
            return Door.already_closed, False

        return "Cannot close this door.", False

    def on_open(self, *_):
        if self.status == Door.Open:
            return Door.already_open, False

        if self.lock is not None:
            if self.lock.is_locked:
                return Door.is_locked, False

        if self.can_close:
            self.status = Door.Open
            return Door.open_success, True

        return "Cannot open this door", False
