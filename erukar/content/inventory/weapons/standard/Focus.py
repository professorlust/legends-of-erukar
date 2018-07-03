import numpy as np
from erukar.system.engine.inventory import ArcaneWeapon


class Focus(ArcaneWeapon):
    Probability = 1
    BaseName = "Focus"
    EssentialPart = "devotion"
    AttackRange = 3
    RangePenalty = 3
    BaseWeight = 1.0

    # Damage
    DamageRange = [2, 5]
    DamageType = 'force'
    DamageModifier = "sense"
    DamageScalar = 2.4
    ScalingRequirement = 6
    EnergyCost = 5

    # Distribution
    Distribution = np.random.gamma
    DistributionProperties = (2, 0.3)


    BaseStatInfluences = {
        'sense':  {'requirement': 8, 'scaling_factor': 3.5, 'cutoff': 200},
        'acuity': {'requirement': 0, 'scaling_factor': 1.2, 'cutoff': 100},
    }

    def failing_requirements(self, wielder):
        if wielder.arcane_energy < self.EnergyCost:
            return ['Not enough Arcane Energy to use {} -- need {}, have {}'.format(self.alias(), self.EnergyCost, wielder.arcane_energy)]

    def on_calculate_attack(self, cmd):
        cmd.args['player_lifeform'].arcane_energy -= self.EnergyCost
