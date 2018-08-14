class SpellMutator:
    def __init__(self, kwargs={}):
        self.allocated = 0
        self.energy = 0
        self.args = kwargs
        self.evasion = None

    def allocate_energy(self, caster):
        self.allocated = caster.allocated_arcane_energy()

    def confirm(self):
        self.energy = self.allocated

    def set(self, kw, val):
        self.args[kw] = val

    def reset(self, kw):
        if kw not in self.args:
            return
        self.args[kw] = type(self.args.get(kw))()

    def remove(self, kw):
        self.args.pop(kw, None)

    def get(self, kw, default=None):
        return self.args.get(kw, default)

    def get_typesafe(self, kw, type, default=None):
        val = self.get(kw)
        if not val or not isinstance(val, type):
            return default
        return val

    def copy(self):
        new_mutator = SpellMutator(self.args.copy())
        new_mutator.allocated = self.allocated
        new_mutator.energy = self.energy
        return new_mutator

    def power(self):
        return self.energy * 0.1

    def power_range(self, lb, ub):
        return (int(self.power() * lb), int(self.power() * ub))

    def perform_mutation(self, target):
        for kw in self.args:
            method = 'mutate_{}'.format(kw)
            if hasattr(target, method):
                mutator = getattr(target, method)
                if kw is 'power':
                    mutator(self.power())
                    continue
                mutator(self.args[kw])
