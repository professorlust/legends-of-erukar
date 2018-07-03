class Condition:
    '''Such as Dead, Dying, Incapacitated, etc.'''
    Incapacitates = False
    IsTemporary = False  # AKA can be tied to a timer
    Persistent = False  # AKA DB Persistent
    Duration = 4
    DamageMitigations = {}
    RemoveOnStartOfTurn = False
    RemoveOnEndOfTurn = False

    Noun = 'Condition'
    Participle = 'Conditioning'
    Description = 'Default Condition Description'

    def __init__(self, target, instigator=None):
        self.target = target
        self.target.conditions.append(self)
        self.instigator = instigator
        self.timer = self.Duration
        self.efficiency = 1.0

    def damage_mitigation(self, damage_type):
        if damage_type in self.DamageMitigations:
            yield self.DamageMitigations[damage_type]

    def duration_remaining(self):
        if self.IsTemporary:
            seconds_left = int(self.timer * 5)
            return '{} seconds'.format(seconds_left)
        return 'Permanent'

    def name(self):
        return self.Noun

    def describe(self):
        return self.Description

    def do_begin_of_turn_effect(self):
        if (self.timer <= 0 or self.Duration == 0) and self.RemoveOnStartOfTurn:
            self.exit()
        return ''

    def do_end_of_turn_effect(self):
        if (self.timer <= 0 or self.Duration == 0) and self.RemoveOnEndOfTurn:
            self.exit()
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

    def on_process_damage(self, attack_state, command):
        pass
