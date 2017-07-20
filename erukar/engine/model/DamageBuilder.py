from .Damage import Damage

class DamageBuilder:
    def __init__(self):
        self.clear()

    def clear(self):
        self.scales = False
        self.name = 'default damage name'
        self.damage = [0, 0]
        self.modifier = ''
        self.distribution = []
        self.dist_params = []
        self.requirement = 8
        self.max_scale = 100
        self.scalar = 1

    def does_scale(self):
        self.scales = True
        return self

    def with_type(self, name):
        self.name = name
        return self

    def with_range(self, damage_range):
        self.damage = damage_range
        return self

    def with_modifier(self, mod):
        self.modifier = mod
        return self

    def with_distribution(self, dist):
        self.distribution = dist
        return self

    def with_properties(self, props):
        self.dist_params = props
        return self

    def with_requirement(self, req):
        self.requirement = req
        return self

    def with_max_scale(self, sc):
        self.max_scale = sc
        return self

    def with_scalar(self, sc):
        self.scalar = sc
        return self

    def build_and_clear(self):
        new_damage = self.build()
        self.clear()
        return new_damage

    def build(self):
        new_damage = Damage()
        new_damage.scales = self.scales
        new_damage.name = self.name
        new_damage.damage = self.damage
        new_damage.modifier = self.modifier
        new_damage.distribution = self.distribution
        new_damage.dist_params = self.dist_params
        new_damage.requirement = self.requirement
        new_damage.max_scale = self.max_scale
        new_damage.scalar = self.scalar
        return new_damage
