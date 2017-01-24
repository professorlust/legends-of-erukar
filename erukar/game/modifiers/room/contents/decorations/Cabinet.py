from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
import random

class Cabinet(RoomModifier):
    Probability = 0.2
    ProbabilityFromFabrication = 1

    materials = [
        "ash",
        "birch",
        "elm",
        "walnut",
        "mohagony"]

    def __init__(self):
        # Need to be able to self-reference 
        self.anomalies = [
            # Description, vision_difficulty, anomaly method
            ("The cabinet is pristine, and looks brand new.", 3, None),
            ("There are scratch marks on the floor near the cabinet.", 10, self.behind_cabinet),
            ("The cabinet has no doors.", 5, self.no_doors),
            ("The doors on the cabinet are locked.", 8, self.add_lock)]

    def apply_to(self, room):
        # set parameters for mutation
        deco = Decoration(aliases=['cabinet'])
        deco.location = self.random_wall(room)
        deco.material = random.choice(self.materials)
        deco.anomaly, vision_difficulty, anomaly_method = random.choice(self.anomalies)
        if anomaly_method is not None: anomaly_method(deco, room)

        # Add Descriptions
        deco.BriefDescription = "a cabinet to the {location}"
        room.add(deco)

    @staticmethod
    def behind_cabinet(deco, room):
        '''Adds a container behind the cabinet which should yield something of high desirability'''
        return

    @staticmethod
    def no_doors(deco, room):
        '''Sets the container to be permanently open'''
        return

    @staticmethod
    def add_lock(deco, room):
        '''Adds a lock to the container, which will allow the dungeon to put a key somewhere.'''
        return
