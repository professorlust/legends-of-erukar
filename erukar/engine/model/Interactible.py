class Interactible:
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
