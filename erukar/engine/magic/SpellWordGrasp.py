class SpellWordGrasp:
    CastCapForMaxEfficiency = 100

    def __init__(self, word_class):
        self.word_class = word_class
        self.successes = 0
        self.total_casts = 0
        self.base_efficiency = 1.0

    def add_cast(self, success=False):
        self.total_casts += 1
        if success: self.successes += 1

    def efficiency(self):
        total, success = map(lambda y: min(y, self.CastCapForMaxEfficiency), [self.total_casts, self.successes])
        return (success / total) * self.base_efficiency
