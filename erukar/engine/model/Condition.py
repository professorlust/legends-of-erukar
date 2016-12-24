class Condition:
    '''Such as Dead, Dying, Incapacitated, etc.'''
    Incapacitates = False
    IsTemporary = False # AKA can be tied to a timer
    Persistent = False # AKA DB Persistent
    Duration = 4

    def __init__(self, target, instigator=None):
        self.target = target
        self.instigator = instigator
        self.timer = self.Duration

    def do_begin_of_turn_effect(self):
        return ''

    def do_end_of_turn_effect(self):
        return ''

    def do_tick_effect(self):
        pass

    def tick(self):
        self.do_tick_effect()
        if self.IsTemporary:
            self.timer -= 1
            if self.timer <= 0:
                self.exit()

    def exit(self):
        self.target.conditions.remove(self)
