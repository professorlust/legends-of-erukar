from erukar.engine.model.RpgEntity import RpgEntity

class Door(RpgEntity):
    close_success = 'You have successfully closed the door'
    open_success = 'You have successfully opened the door'
    already_closed = 'The door is already closed'
    open_success = 'You have successfully opened the door'
    is_locked = 'You try to open the door, but it is locked'
    already_open = 'The door is already open'
    Closed = 0
    Open = 1

    def __init__(self, description=""):
        '''description should allow a {0} for formatting direction'''
        self.lock = None
        self.status = Door.Closed
        self.can_close = True
        self.description = description

    def on_inspect(self, direction):
        if self.description != "":
            return self.description.format(direction)
        return self.on_inspect_generic(direction)

    def on_inspect_generic(self, direction):
        return "There is a door to the {0}".format(direction)

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
