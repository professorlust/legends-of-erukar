import random

class GenerationProfile:
    def __init__(self, temperature=0, altitude=0, fabrication=0, sanctity=0):
        ''' All of these values should exist on the interval -1 < x < +1 '''
        # Where -1 is arctic and +1 is volcanic
        self.temperature = temperature

        # Where -1 is subterranean and +1 is on top of the highest mountain
        self.altitude = altitude

        # Where -1 is natural and +1 is completely manmade
        self.fabrication = fabrication

        # Where -1 is infernal and +1 is celestial
        self.sanctity = sanctity

    def random():
        return GenerationProfile(*((random.random()*2)-1 for x in range(4)))
