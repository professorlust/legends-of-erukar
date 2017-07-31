class Damage:
    Types = [
        'piercing',
        'bludgeoning',
        'slashing',
        'fire',
        'ice',
        'electric',
        'acid',
        'force',
        'divine',
        'demonic',
    ]

    def __init__(self):
        self.scales = False
        self.name = 'default damage name -- use DamageBuilder'
        self.damage = [0, 0]
        self.modifier = ''
        self.distribution = []
        self.dist_params = []
        self.requirement = 8
        self.max_scale = 100
        self.scalar = 1

    def roll(self, attacker):
        # Get a random value from the distribution passed in 
        random_val = self.distribution(*self.dist_params)
        # Scale the value between the boundary rangess
        raw = numpy.round((self.damage[1] - self.damage[0]) * random_val) + self.damage[0]
        # Do we have a modifier for this value? if so, apply it
        if hasattr(attacker, self.modifier) and self.scales:
            return int(raw) + getattr(attacker, self.modifier)
        return int(raw)

    def scaled_values(self, for_player, weapon=None):
        '''Returns a tuple of low to high range of damage'''
        return tuple(self.scale(for_player, damage, weapon) for damage in self.damage)

    def scale(self, for_player, value, weapon):
        '''Performs a scalar adjustment on a value'''
        if not self.scales: return value
        # If we don't meet requirements, just ignore this
        stat = getattr(for_player, self.modifier)
        if stat < self.requirement: return 1
        # Get the adjusted value
        adj_max_scale = self.max_scale + for_player.offset_scale(weapon)
        adj_scale = self.adjusted_scalar(for_player, weapon)
        actual_scale = (1 + min(adj_max_scale, (stat - self.requirement))) * adj_scale
        return int(actual_scale) + value

    def adjusted_scalar(self, for_player, weapon):
        if not self.scales: return value
        return self.scalar + for_player.offset_scale(weapon)

    @staticmethod
    def actual_damage_values(instigator, enemy, weapon, damages):
        '''Determine the actual damage amount dealt after deflection and mitigation'''
        for damage_amount, damage_type in damages:
            # Calculate the unmitigated damage
            actual_damage = int(enemy.mitigation(damage_type) * damage_amount)
            damage_taken_by_armor = int(damage_amount) - actual_damage
            # Mitigated damage is reflected back to the weapon if it exists
            if weapon is not None:
                weapon.take_damage(damage_taken_by_armor)
            enemy.damage_armor(damage_taken_by_armor)
            # After mitigation, if there is any remaining damage, the lifeform takes that in health
            if actual_damage > 0:
               yield (actual_damage, damage_type)

    @staticmethod
    def deflections(instigator, enemy, damages):
        for damage_amount, damage_type in damages:
            if hasattr(enemy, 'deflection') and enemy.deflection(damage_type) >= damage_amount:
                yield damage_type
