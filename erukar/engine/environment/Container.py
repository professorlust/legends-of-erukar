from erukar.engine.model.Containable import Containable
from erukar.engine.environment.Lock import Lock
import random

class Container(Containable):
    def __init__(self, aliases):
        '''visible_in_room_description here is used for Containers like Table Tops'''
        super().__init__(aliases)
        self.visible_in_room_description = True
        self.can_close = True
        self.contents_visible = False
        self.lock = None

    def on_open(self, sender):
        if not self.can_close:
            return self.mutate("You cannot open this {alias}.")

        if self.lock is not None:
            if self.lock.is_locked:
                return self.mutate("This {alias} is locked!")

        self.contents_visible = True
        return self.mutate("Opened a {alias}.")

    def on_start(self, room):
        for content in self.contents:
            content.on_start(room)

    def on_close(self, sender):
        if self.can_close:
            self.contents_visible = False
            return self.mutate("Closed a {alias}")
        return self.mutate("{alias} cannot be closed!")

    def brief_inspect(self, lifeform, acu, sen, content_desc_format='{},'):
        if not self.visible_in_room_description: return ''
        return super().brief_inspect(lifeform, acu, sen)

    def content_brief_descriptions(self, lifeform, acu, sen, content_format=', '):
        content_results = [x.brief_inspect(lifeform, acu, sen) for x in self.contents if x is not lifeform]
        return content_format.join([x for x in content_results if x is not ''])

    def glance_inside_from_inspect_no_preface(self):
        return self.glance_inside(no_preface=True, from_inspect=True)

    def glance_inside_from_inspect(self):
        return self.glance_inside(from_inspect=True)

    def glance_inside_no_preface(self):
        return self.glance_inside(no_preface=True)

    def glance_inside(self, no_preface=False, from_inspect=False):
        if len(self.contents) > 0 and self.contents_visible:
            # The following should be reworked to show the most visible items
            acuity = random.uniform(0, 50)
            sense = random.uniform(0, 50)
            visible = random.choice(self.contents).on_glance(None, acuity, sense)
            if no_preface:
                return visible
            if visible is not '':
                preface = self.on_inspect_preface if from_inspect else self.on_glance_prefix
                return preface.format(visible)
        return ''
