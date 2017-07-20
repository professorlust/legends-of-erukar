from erukar.engine.inventory.Weapon import Weapon
import numpy as np
import random

class Wand(Weapon):
    Probability = 1
    BaseName = "Wand"
    EssentialPart = "tip"
    AttackRange = 2
    RangePenalty = 2
    BaseWeight = 1.0

    # Damage
    DamageRange = [1, 4]
    DamageType = 'force'
    DamageModifier = "acuity"
    DamageScalar = 2.4
    ScalingRequirement = 6
    EnergyCost = 5

    # Distribution
    Distribution = np.random.gamma
    DistributionProperties = (2, 0.3)


    BaseStatInfluences = {
        'acuity':  {'requirement': 8, 'scaling_factor': 3, 'cutoff': 200},
        'dexterity': {'requirement': 0, 'scaling_factor': 1.5, 'cutoff': 200},
    }

    def failing_requirements(self, wielder):
        if wielder.arcane_energy < self.EnergyCost:
            return ['Not enough Arcane Energy to use {} -- need {}, have {}'.format(self.alias(), self.EnergyCost, wielder.arcane_energy)]

    def on_calculate_attack(self, cmd):
        cmd.args['player_lifeform'].arcane_energy -= self.EnergyCost
