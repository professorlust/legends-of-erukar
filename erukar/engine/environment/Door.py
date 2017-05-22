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
        self.is_open = False
        self.can_open_or_close = True
        self.description = description
        self.acuity_needed = 0
        if self.description is '':
            self.description = self.generic_description

    def alias(self):
        return 'door'

    def on_inspect(self, direction):
        return self.mutate(self.description, {'direction': direction.name})

    def on_glance(self, player):
        return 'Glanced at a door: {} ACU, {} SEN'.format(player.acuity, player.sense), True

    def peek(self, direction, room, lifeform, acu, sen):
        '''Does a single look through'''
        if self.is_open and room is not None:
            return ' '.join([self.on_inspect(direction), room.peek(lifeform, acu, sen)])
        return self.on_inspect(direction)

    def necessary_acuity(self):
        return self.acuity_needed

    def describe_locked(self):
        if self.lock is None:
            return ''
        return self.lock.describe()

    def describe_lock(self, direction=None):
        if self.lock is not None:
            return self.mutate(self.lock.description)
        return ''

    def can_close(self):
        return self.can_open_or_close and self.is_open

    def can_open(self):
        return self.can_open_or_close and not self.is_open and (self.lock is None or not self.lock.is_locked)

    def on_close(self, player):
        if self.can_close():
            self.is_open = False
            return Door.close_success, True

        return "Cannot close this door.", False

    def on_open(self, *_):
        if self.can_open():
            self.is_open = True
            return Door.open_success, True

        return "Cannot open this door", False
