from erukar.system.engine import Condition


class Enraged(Condition):
    IsTemporary = True
    Duration = 10  # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun = 'Enraged'
    Participle = 'Raging'
    Description = 'Adds Total Resolve Score to attack rolls, physical '\
        'damage, and physical mitigation but reduces sense and acuity '\
        'by the same amount'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        if instigator is None:
            instigator = target
        self.resolve_amount = 0

    def modify_acuity(self, *_):
        return -self.resolve_amount

    def modify_sense(self, *_):
        return -self.resolve_amount

    def modify_strength(self, *_):
        return self.resolve_amount

    def modify_vitality(self, *_):
        return self.resolve_amount
