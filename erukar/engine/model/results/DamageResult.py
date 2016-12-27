import erukar

class DamageResult:
    def __init__(self, victim, instigator):
        self.reports = []
        self.victim = victim
        self.init_instigator(instigator)
        self.caused_incapacitated = False
        self.caused_death = False
        self.stopped_by_deflection = False
        self.stopped_by_mitigation = False
        self.xp_value = 0

    def init_instigator(self, instigator):
        '''Allows us to figure out if a trap caused this or a lifeform'''
        self.is_trap = not hasattr(instigator, 'uid')
        if not self.is_trap:
            self.instigator = instigator.uid

    def parse_status(self):
        '''Figure out what we did and figure out if to award XP'''
        self.stopped_by_deflection = all(x.stopped_by_deflection for x in self.reports)
        self.stopped_by_mitigation = all(x.stopped_by_mitigation for x in self.reports)

        if not issubclass(type(self.victim), erukar.engine.lifeforms.Lifeform): return
        self.caused_incapacitated = self.victim.has_condition(erukar.engine.conditions.Dying)
        self.caused_death = self.victim.has_condition(erukar.engine.conditions.Dead)
        print((self.caused_incapacitated, self.caused_death))
        if self.caused_death and not self.is_trap:
            self.xp_value = self.victim.calculate_xp_worth()
