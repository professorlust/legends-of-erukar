class Condition:
    '''Such as Dead, Dying, Incapacitated, etc.'''
    Incapacitates = False
    Persistent = False

    def __init__(self, target, instigator=None):
        self.target = target
        self.instigator = instigator

    def do_begin_of_turn_effect(self):
        return ''

    def do_end_of_turn_effect(self):
        return ''

    def tick(self):
        pass
