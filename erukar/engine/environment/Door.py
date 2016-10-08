from erukar.engine.model.Describable import Describable

class Door(Describable):
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
        self.lock = None
        self.status = Door.Closed
        self.can_close = True
        self.description = description
        self.acuity_needed = 0
        if self.description is '':
            self.description = self.generic_description

    def on_inspect(self, direction):
        return self.mutate(self.description, {'direction': direction.name})

    def peek(self, direction, room, lifeform, acu, sen):
        '''Does a single look through'''
        if self.status is Door.Open:
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

    def describe_lock(self, direction):
        if self.lock.direction is direction:
            args = {
                'door': self.description.format(direction),
                'lockname': self.lock.alias(),
                'lock': self.lock.on_inspect()}
            return '{door} Attached to the door is a {lockname}. {lock}'.format(**args)
        return '{door} The door does not open.'.format(self.description.format(direction))

    def on_close(self, player):
        if self.can_close:
            if self.status == Door.Open:
                self.status = Door.Closed
                return Door.close_success
            return Door.already_closed

        return "Cannot close this door."

    def on_open(self, *_):
        if self.status == Door.Open:
            return Door.already_open

        if self.lock is not None:
            if self.lock.is_locked:
                return Door.is_locked

        if self.can_close:
            self.status = Door.Open
            return Door.open_success

        return "Cannot open this door"
