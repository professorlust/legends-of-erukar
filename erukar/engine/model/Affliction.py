class Affliction:
    '''Such as Dead, Dying, Incapacitated, etc.'''
    Incapacitates = False

    def __init__(self, afflicted, instigator=None):
        self.afflicted = afflicted
        self.instigator = instigator

    def do_begin_of_turn_effect(self):
        return ''

    def do_end_of_turn_effect(self):
        return ''
