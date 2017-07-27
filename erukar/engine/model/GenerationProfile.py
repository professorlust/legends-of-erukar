import math, functools, operator

class GenerationProfile():
    def __init__(self, **kwargs):
        super().__init__()
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])

    def stochasticity_weight(self, profile):
        weights = [
            getattr(self, parameter).variable_correlation(getattr(profile, parameter, -math.inf))\
            for parameter in profile.__dict__.keys() if hasattr(self, parameter)
        ]
        return sum(weights) / len([getattr(self, parameter).strength for parameter in profile.__dict__.keys() if hasattr(self, parameter)])
