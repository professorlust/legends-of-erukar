from erukar.system.engine import Damage, DamageScalar
from ..Weapon import Weapon


class MartialWeapon(Weapon):
    '''Intended for weapons with physical components only'''
    SlashingPercentage = 0.00
    PiercingPercentage = 0.00
    BludgeoningPercentage = 0.00
    DamageVariance = 0.50
    RawBase = 10
    MaximumRange = 1.5
    ModifierPath = 'erukar.content.modifiers.melee'

    def bludgeon_damage_scalars(self):
        yield DamageScalar(
            self.raw_base_damage(),
            'strength',
            percentage=self.bludgeoning_percentage())

    def piercing_damage_scalars(self):
        yield DamageScalar(
            self.raw_base_damage(),
            'dexterity',
            percentage=self.piercing_percentage())

    def slashing_damage_scalars(self):
        yield DamageScalar(
            self.raw_base_damage(),
            'dexterity',
            percentage=self.slashing_percentage())

    def get_base_damages(self):
        if self.bludgeoning_percentage() > 0.00:
            yield Damage('bludgeoning', list(self.bludgeon_damage_scalars()))

        if self.piercing_percentage() > 0.00:
            yield Damage('piercing', list(self.piercing_damage_scalars()))

        if self.slashing_percentage() > 0.00:
            yield Damage('slashing', list(self.slashing_damage_scalars()))

    def bludgeoning_percentage(self):
        pct = self.BludgeoningPercentage
        for modifier in self.modifiers:
            if hasattr(modifier, 'modify_bludgeoning_percentage'):
                pct = modifier.modify_bludgeoning_percentage(self, pct)
        return pct

    def piercing_percentage(self):
        pct = self.PiercingPercentage
        for modifier in self.modifiers:
            if hasattr(modifier, 'modify_piercing_percentage'):
                pct = modifier.modify_piercing_percentage(self, pct)
        return pct

    def slashing_percentage(self):
        pct = self.SlashingPercentage
        for modifier in self.modifiers:
            if hasattr(modifier, 'modify_slashing_percentage'):
                pct = modifier.modify_slashing_percentage(self, pct)
        return pct
