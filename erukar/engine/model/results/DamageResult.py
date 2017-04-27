import erukar

class DamageResult:
    def __init__(self, target, instigator):
        self.reports = []
        self.target = target
        self.init_instigator(instigator)
        self.caused_incapacitated = False
        self.caused_death = False
        self.stopped_by_deflection = False
        self.stopped_by_mitigation = False
        self.xp_value = 0

    def init_instigator(self, instigator):
        self.is_trap = not hasattr(instigator, 'uuid')
        self.instigator = instigator

    def parse_status(self):
        '''Figure out what we did and figure out if to award XP'''
        self.stopped_by_deflection = all(x.stopped_by_deflection for x in self.reports)
        self.stopped_by_mitigation = all(x.stopped_by_mitigation for x in self.reports)

        if not issubclass(type(self.target), erukar.engine.lifeforms.Lifeform): return

        already_incapacitated = self.target.has_condition(erukar.engine.conditions.Dying)
        total_damage = self.get_damage_total()

        self.caused_incapacitated = not already_incapacitated and total_damage >= self.target.health
        self.caused_death = already_incapacitated and total_damage > 0
        if self.caused_death and not self.is_trap:
            self.xp_value = self.target.calculate_xp_worth()

    def get_damage_total(self):
        return sum([report.amount_dealt for report in self.reports])

    def merge(self, other):
        self.reports.extend(other.reports)
        self.caused_incapacitated = self.caused_incapacitated or other.caused_incapacitated
        self.caused_death = self.caused_death or other.caused_death
        self.stopped_by_deflection = self.stopped_by_deflection or other.stopped_by_deflection
        self.stopped_by_mitigation = self.stopped_by_mitigation or other.stopped_by_mitigation

        self.xp_value += other.xp_value
