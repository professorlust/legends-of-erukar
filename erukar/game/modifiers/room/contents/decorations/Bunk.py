from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
import random

class Bunk(RoomModifier):
    Probability = 0.2
    ProbabilityFromFabrication = 0.7

    bed_states = [
        "oversized",
        "cheaply made",
        "extravagant",
        "ornate",
        "nicely made",
        "bare",
        "disheveled",
        "covered with garbage",
        "collapsed"]

    bed_smells = [
        # (DC, smell description)
        (5, 'clean linen'),
        (8, 'an unidentifiable, yet pleasant scent'),
        (15, 'rotting cloth'),
        (10, 'decay'),
        (8, 'something repugnant'),
        (20, 'death')]

    def apply_to(self, room):
        deco = Decoration(aliases=['bunk'])
        deco.bed_state = random.choice(self.bed_states)
        smell_difficulty, deco.bed_smell = random.choice(self.bed_smells)
        deco.location = self.random_wall(room)
        deco.BriefDescription = "a bunk on the {location} side of the room"
        room.add(deco)
