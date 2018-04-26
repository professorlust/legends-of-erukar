from erukar.system.engine import Damage, Weapon, DamageScalar

class MartialWeapon(Weapon):
    '''Intended for weapons with physical components only'''
    SlashingPercentage    = 0.00
    PiercingPercentage    = 0.00
    BludgeoningPercentage = 0.00
    DamageVariance        = 0.50
    RawBase               = 10

    def bludgeoning_damage_scalars(self):
        yield DamageScalar(self.RawBase, 'strength', percentage=self.BludgeoningPercentage)

    def piercing_damage_scalars(self):
        yield DamageScalar(self.RawBase, 'dexterity', percentage=self.PiercingPercentage)

    def slashing_damage_scalars(self):
        yield DamageScalar(self.RawBase, 'dexterity', percentage=self.SlashingPercentage)

    def get_base_damages(self):
        if self.BludgeoningPercentage > 0.00:
            yield Damage('bludgeoning', list(self.bludgeoning_damage_scalars()))

        if self.PiercingPercentage > 0.00:
            yield Damage('piercing', list(self.piercing_damage_scalars()))

        if self.SlashingPercentage > 0.00:
            yield Damage('slashing', list(self.slashing_damage_scalars()))

