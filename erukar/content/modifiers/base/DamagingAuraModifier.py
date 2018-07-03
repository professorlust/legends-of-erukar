from .AuraModifier import AuraModifier
from erukar.system.engine import Damage, DamageScalar, Lifeform


class DamagingAuraModifier(AuraModifier):
    DamageType = 'arcane'
    RawDamage = 10
    ScalarStat = 'acuity'
    ScaleAmount = 1.5
    Requirement = 0

    def modify_aura(self):
        self.aura.tick = self.tick

    def tick(self):
        if not self.aura.initiator:
            return
        initiator = self.aura.initiator
        for target in self.valid_targets(initiator):
            strength = self.aura.strength_at(target.coordinates)
            damage = Damage(
                self.DamageType,
                [DamageScalar(
                    self.RawDamage * strength,
                    self.ScalarStat,
                    scale_amount=self.ScaleAmount,
                    requirement=self.Requirement
                )])
            target.apply_damage(initiator, None, damage)

    def valid_targets(self, initiator):
        origin = self.aura.location
        radius = self.max_distance
        for actor in self.actors_in_range(origin, radius):
            if not isinstance(actor, Lifeform):
                continue
            if actor.is_hostile_to(initiator):
                yield actor
