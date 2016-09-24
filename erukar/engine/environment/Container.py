from erukar.engine.model.Containable import Containable
from erukar.engine.environment.Lock import Lock

class Container(Containable):
    ContentDescription = "Inside of the container is {}."


    def __init__(self, aliases):
        '''visible_in_room_description here is used for Containers like Table Tops'''
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

    def brief_inspect(self, lifeform, acu, sen, content_desc_format='{},'):
        if not self.visible_in_room_description: return ''
        return super().brief_inspect(lifeform, acu, sen)

    def on_inspect(self, lifeform, acu, sen):
        self_desc = self.describe_base(lifeform, acu, sen) 
        content_desc = self.content_brief_descriptions(lifeform, acu, sen)
        return '\n\n'.join([self_desc, self.ContentDescription.format(content_desc)])

    def content_brief_descriptions(self, lifeform, acu, sen, content_format=', '):
        content_results = [x.brief_inspect(lifeform, acu, sen) for x in self.contents if x is not lifeform]
        return content_format.join([x for x in content_results if x is not ''])
