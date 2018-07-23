class Damage:
    Types = [
        'bludgeoning',
        'piercing',
        'slashing',
        'fire',
        'ice',
        'electric',
        'aqueous',
        'arcane',
        'force',
        'divine',
        'demonic',
    ]

    def __init__(self, damage_type, scalars=[]):
        self.damage_type = damage_type
        self.scalars = scalars

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

    def raw_scaled_for(self, lifeform):
        return sum([s.scale_for(lifeform) for s in self.scalars])

    @staticmethod
    def ordered(damage_dict):
        for _type in Damage.Types:
            if _type in damage_dict:
                yield '{} {}'.format(damage_dict[_type], _type)
