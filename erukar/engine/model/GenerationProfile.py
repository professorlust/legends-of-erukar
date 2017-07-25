import random

class GenerationProfile:
    def Woodlands():
        return GenerationProfile(
            plant_growth =  0.8,
            moisture     =  0.4,
            temperature  =  0.2,
            altitude     =  0.1,
            sanctity     =  0.0,
            fabrication  = -0.4,
        )

    def __init__(self, **kwargs):
        ''' All of these values should exist on the interval -1 < x < +1 '''
        self.altitude = 0
        self.fabrication = 0
        self.moisture = 0
        self.plant_growth = 0
        self.sanctity = 0
        self.temperature = 0

        for kw in kwargs:
            if hasattr(self, kw):
                setattr(self, kw, kwargs[kw])
