from erukar.engine.environment.Lock import Lock
from erukar.engine.calculators.Random import Random
import numpy as np

class TieredLock(Lock):
    Tiers = [
        # Material, Prevalence
        ('Iron',1),
        ('Steel',2),
        ('Copper',4),
        ('Bronze',8),
        ('Silver',16),
        ('Gold', 32),
        ('Platinum', 64),
        ('Diamond', 128)
    ]

    def __init__(self, difficulty):
        possibilities, weights = zip(*[(tier, 1/(value*2)) for tier,value in self.Tiers])
        bins, values = Random.create_random_distribution(possibilities, weights)
        random = float(np.random.beta(10/difficulty, 5))
        self.tier = Random.get_from_custom_distribution(random, bins, values)
