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

    def do_begin_of_turn_effect(self, cmd):
        if self.expired() and self.RemoveOnStartOfTurn:
            self.exit()

    def do_end_of_turn_effect(self, cmd):
        if self.expired() and self.RemoveOnEndOfTurn:
            self.exit()

    def expired(self):
        return self.IsTemporary and (self.timer <= 0 or self.Duration == 0)

    def do_tick_effect(self, cmd):
        pass

    def tick(self, cmd):
        self.do_tick_effect(cmd)
        if self.IsTemporary:
            self.timer -= 1
            if self.expired():
                cmd.append_result(
                    self.target.uid,
                    '{} expires.'.format(self.name()))
                self.exit()

    def exit(self):
        self.target.conditions.remove(self)

    def on_process_damage(self, attack_state, command):
        pass
