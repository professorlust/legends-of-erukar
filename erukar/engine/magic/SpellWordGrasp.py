class SpellWordGrasp:
    CastCapForMaxEfficiency = 100

    def __init__(self, word_class, successes=0, total=0):
        self.word_class = word_class
        self.successes = 0
        self.total = 0
        self.base_efficiency = 1.0
        self.max_efficiency  = 1.0

    def add_cast(self, success=False):
        self.total += 1
        if success: self.successes += 1

    def efficiency(self):
        total, success = map(lambda y: min(y, self.CastCapForMaxEfficiency), [self.total, self.successes])
        proportion = 0 if total == 0 else success/total
        return self.base_efficiency + proportion * (self.max_efficiency - self.base_efficiency)
