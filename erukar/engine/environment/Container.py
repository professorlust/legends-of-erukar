from erukar.engine.model.Containable import Containable
from erukar.engine.environment.Lock import Lock

class Container(Containable):
    def __init__(self, aliases):
        super().__init__(aliases)
        self.visible_in_room_description = True
        self.can_close = True
        self.contents_visible = False
        self.lock = None

    def on_open(self, sender):
        if not self.can_close:
            return "You cannot open this container"

        if self.lock is not None:
            if self.lock.is_locked:
                return "This container is locked!"

        self.contents_visible = True
        return "Opened a chest"

    def on_start(self, room):
        for content in self.contents:
            content.on_start(room)

    def on_close(self, sender):
        if self.can_close:
            self.contents_visible = False
            return "Closed a chest"
        return "Cannot close this container"

    def brief_inspect(self, lifeform, acu, sen):
        if not self.visible_in_room_description: return ''
        content_results = [x.brief_inspect(lifeform, acu, sen) for x in self.contents if x is not lifeform]
        descriptions = ' '.join(['You see {}.'.format(x) for x in content_results if x is not ''])
        return 'In this {}...{}'.format(self.alias(),  descriptions)

    def on_inspect(self, *_):
        return 'Container Full Inspect'
