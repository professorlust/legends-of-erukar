from erukar.system.engine import Describable, Containable
from .Lock import Lock
import random

class Container(Containable):
    Opened = "Opened a Chest"

    def __init__(self, aliases):
        '''visible_in_room_description here is used for Containers like Table Tops'''
        super().__init__(aliases)
        self.on_glance_prefix = ''
        self.on_inspect_prefix = ''
        self.visible_in_room_description = True
        self.is_open = False
        self.lock = None
        self.can_open_or_close = True

    def can_close(self):
        return self.can_open_or_close and self.is_open

    def can_open(self):
        return self.can_open_or_close and not self.is_open and (self.lock is None or not self.lock.is_locked)

    def on_open(self, sender):
        if not self.can_close:
            return self.mutate("You cannot open this {alias}."), False

        if self.lock is not None:
            if self.lock.is_locked:
                return self.mutate("This {alias} is locked!"), False

        self.is_open = True
        return self.mutate(Container.Opened), True

    def on_start(self, room):
        for content in self.contents:
            content.on_start(room)

    def on_close(self, sender):
        if self.can_close():
            self.is_open = False
            return self.mutate("Closed a {alias}"), False
        return self.mutate("{alias} cannot be closed!"), False

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
        if len(self.contents) > 0 and self.is_open:
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

    def on_inspect(self, player, acuity, sense):
        if self.is_open:
            return super().on_inspect(player, acuity, sense)
        return self.mutate(Describable.get_best_match(self.Inspects, acuity, sense))
