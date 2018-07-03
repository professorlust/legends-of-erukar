from erukar.system.engine import Damage, DamageScalar
from ..Weapon import Weapon


class ArcaneWeapon(Weapon):
    ModifierPath = 'erukar.content.modifiers.ranged'

    def get_base_damages(self):
        yield Damage('force', list(self.force_damage_scalars()))

    def force_damage_scalars(self):
        yield DamageScalar(self.raw_base_damage(), 'acuity', percentage=1.00)
