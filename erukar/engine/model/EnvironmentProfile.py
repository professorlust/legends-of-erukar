import random

class EnvironmentProfile:
    def Woodlands():
        return EnvironmentProfile(
            plant_growth =  0.8,
            moisture     =  0.4,
            temperature  =  0.2,
            altitude     =  0.1,
            sanctity     =  0.0,
            fabrication  = -0.4,
        )

    def AridDesert():
        return EnvironmentProfile(
            plant_growth = -0.9,
            moisture     = -1.0,
            temperature  =  0.8,
            altitude     =  0.0,
            sanctity     =  0.0,
            fabrication  = -1.0,
        )

    def Tundra():
        return EnvironmentProfile(
            plant_growth = -0.9,
            moisture     = -0.3,
            temperature  = -1.0,
            altitude     = -0.3,
            sanctity     =  0.0,
            fabrication  = -1.0,
        )

    def CityOutdoors():
        return EnvironmentProfile(
            plant_growth = -0.2,
            moisture     = -0.1,
            temperature  =  0.4,
            altitude     =  0.3,
            sanctity     =  0.3,
            fabrication  =  0.8,
        )

    def __init__(self, **kwargs):
        ''' All of these values should exist on the interval -1 < x < +1 '''
        self.altitude     = 0.0
        self.fabrication  = 0.0
        self.moisture     = 0.0
        self.plant_growth = 0.0
        self.sanctity     = 0.0
        self.temperature  = 0.0

        for kw in kwargs:
            if hasattr(self, kw):
                setattr(self, kw, kwargs[kw])
