from erukar.system.engine import Weapon, Damage, DamageScalar

class ArcaneWeapon(Weapon):
    def get_base_damages(self):
        yield Damage('force', list(self.force_damage_scalars()))

    def force_damage_scalars(self):
        yield DamageScalar(self.RawBase, 'acuity', percentage=1.00)
