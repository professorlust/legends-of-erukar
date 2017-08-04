import random

class EnvironmentProfile:
    def Woodlands():
        return EnvironmentProfile(
            fertility     =  0.8,
            ambient_water =  0.4,
            temperature   =  0.4,
            altitude      =  0.1,
            sanctity      =  0.0,
            fabrication   = -0.4,
            shelter       = -1.0
        )

    def AridDesert():
        return EnvironmentProfile(
            fertility     = -0.9,
            ambient_water = -1.0,
            precipitation = -1.0,
            temperature   =  0.8,
            fabrication   = -1.0,
            shelter       = -1.0,
            barrenness    =  1.0
        )

    def Tundra():
        return EnvironmentProfile(
            fertility     = -0.9,
            precipitation = -0.9,
            ambient_water =  0.1,
            temperature   = -1.0,
            altitude      = -0.3,
            sanctity      =  0.0,
            fabrication   = -1.0,
            shelter       = -1.0,
            barrenness    =  0.6
        )

    def SnowyWoodlands():
        return EnvironmentProfile(
            fertility     =  0.6,
            precipitation =  1.0,
            ambient_water =  0.4,
            temperature   = -0.8,
            altitude      = -0.3,
            sanctity      =  0.0,
            fabrication   = -0.8,
            shelter       = -1.0,
            barrenness    = -0.7
        )

    def Snowy():
        return EnvironmentProfile(
            fertility     = -0.5,
            precipitation =  1.0,
            ambient_water =  0.0,
            temperature   = -0.8,
            altitude      = -0.3,
            sanctity      =  0.0,
            fabrication   = -1.0,
            shelter       = -0.5,
        )

    def CityOutdoors():
        return EnvironmentProfile(
            fertility     = -0.2,
            precipitation = -0.1,
            ambient_water =  0.3,
            temperature   =  0.4,
            altitude      =  0.3,
            sanctity      =  0.3,
            fabrication   =  0.5,
            wealth        =  0.1,
            shelter       =  0.0
        )

    def CityIndoors():
        return EnvironmentProfile(
            fertility     = -1.0,
            precipitation = -0.4,
            ambient_water =  0.0,
            temperature   =  0.3,
            altitude      =  0.1,
            sanctity      =  0.4,
            fabrication   =  1.0,
            wealth        =  0.4,
            shelter       =  1.0
        )

    def __init__(self, **kwargs):
        ''' All of these values should exist on the interval -1 < x < +1 '''
        self.altitude      = 0.0 # -1.0 is the deepest mine, 1.0 is the top of a mountain
        self.precipitation = 0.0 # -1.0 is a terrible drought, 1.0 is a monsoon or blizzard
        self.ambient_water = 0.0 # How much water is normally availabe in the environment (excluding precipitation) -1.0 is a desert, 1.0 is an ocean
        self.wind          = 0.0 # -1.0 is no wind ever, 0.0 is a light breeze, and 1.0 is a hurricane or tornado
        self.fertility     = 0.0 # -1.0 is incapable of growth, 1.0 is a dense jungle
        self.barrenness    = 0.0
        self.sanctity      = 0.0 # Do Demons (-1.0) walk this area, do Gods (1.0)? If neither, 0.0 is probably the best choice
        self.temperature   = 0.0 # How warm is the environment? 0.3 is room temperature.

        # Parameters in establishments
        self.fabrication   = 0.0 # How many structures are we likely to see? -1.0 is none, 1.0 is likely indoors
        self.wealth        = 0.0 # How rich is the area?
        self.maintenance   = 0.0 # How well kept is this area?
        self.shelter       = 0.0 # Is this indoors, or outdoors?
        self.structure_age = 0.0 # How old are structures here (if they exist)? -1.0 is brand new, 1.0 is ancient

        for kw in kwargs:
            if hasattr(self, kw):
                setattr(self, kw, kwargs[kw])
