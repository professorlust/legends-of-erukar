import uuid

class ErukarObject:
    def __init__(self):
        self.uuid = uuid.uuid4()

    def get_object_by_uuid(self, uuid):
        if uuid == self.uuid: 
            return self

    def is_detected(self, acuity, sense):
        return acuity > self.minimum_acuity_to_detect() or sense > self.minimum_sense_to_detect()

    def minimum_sense_to_detect(self):
        return 1

    def minimum_acuity_to_detect(self):
        return 1

    def on_inspect(self, sender):
        pass

    def on_start(self, *_):
        pass

    def on_attack(self, sender):
        pass

    def on_equip(self, sender):
        pass

    def on_move(self, sender):
        pass

    def on_take(self, sender):
        pass

    def on_open(self, sender):
        pass

    def on_close(self, sender):
        pass

    def on_use(self, sender):
        pass

    def on_give(self, sender):
        pass

    def matches(self, other):
        return False

    def get_name(self):
        pass

    def hear(self):
        pass

    def take_damage(self, damage, instigator=None):
        pass

    def on_hear(self, sound, decay=1.0, instigator=None, direction=None):
        pass
