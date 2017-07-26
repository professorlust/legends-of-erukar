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
            shelter      = -1.0
        )

    def AridDesert():
        return EnvironmentProfile(
            plant_growth = -0.9,
            moisture     = -1.0,
            temperature  =  0.8,
            altitude     =  0.0,
            sanctity     =  0.0,
            fabrication  = -1.0,
            shelter      = -1.0
        )

    def Tundra():
        return EnvironmentProfile(
            plant_growth = -0.9,
            moisture     = -0.3,
            temperature  = -1.0,
            altitude     = -0.3,
            sanctity     =  0.0,
            fabrication  = -1.0,
            shelter      = -1.0
        )

    def SnowyWoodlands():
        return EnvironmentProfile(
            plant_growth =  0.6,
            moisture     =  0.7,
            temperature  = -0.5,
            altitude     = -0.3,
            sanctity     =  0.0,
            fabrication  = -0.8,
            shelter      = -1.0
        )

    def Snowy():
        return EnvironmentProfile(
            plant_growth = -0.5,
            moisture     =  0.7,
            temperature  = -0.5,
            altitude     = -0.3,
            sanctity     =  0.0,
            fabrication  = -1.0,
            shelter      = -0.5
        )

    def CityOutdoors():
        return EnvironmentProfile(
            plant_growth = -0.2,
            moisture     = -0.1,
            temperature  =  0.4,
            altitude     =  0.3,
            sanctity     =  0.3,
            fabrication  =  0.5,
            opulence     =  0.1,
            shelter      =  0.0
        )

    def CityIndoors():
        return EnvironmentProfile(
            plant_growth = -1.0,
            moisture     = -0.4,
            temperature  =  0.3,
            altitude     =  0.1,
            sanctity     =  0.4,
            fabrication  =  1.0,
            opulence     =  0.4,
            shelter      =  1.0
        )

    def __init__(self, **kwargs):
        ''' All of these values should exist on the interval -1 < x < +1 '''
        self.altitude     = 0.0 # -1.0 is the deepest mine, 1.0 is the top of a mountain
        self.moisture     = 0.0 # -1.0 has never seen water, 1.0 is an ocean
        self.plant_growth = 0.0 # -1.0 is incapable of growth, 1.0 is a dense jungle
        self.sanctity     = 0.0 # Do Demons (-1.0) walk this area, do Gods (1.0)? If neither, 0.0 is probably the best choice
        self.temperature  = 0.0 # How warm is the environment? 0.3 is room temperature.

        # Parameters in establishments
        self.fabrication  = 0.0 # How many structures are we likely to see? -1.0 is none, 1.0 is likely indoors
        self.opulence     = 0.0 # How rich is the area?
        self.maintenance  = 0.0 # How well kept is this area?
        self.shelter      = 0.0 # Is this indoors, or outdoors?

        for kw in kwargs:
            if hasattr(self, kw):
                setattr(self, kw, kwargs[kw])
