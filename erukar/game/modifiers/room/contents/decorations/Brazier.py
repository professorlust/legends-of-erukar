from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment import *
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import erukar, random

class Brazier(RoomModifier):
    Probability = 0.2
    ProbabilityFromFabrication = 0.5
    materials = [
        'brass',
        'bronze',
        'copper',
        'iron'
    ]

    def __init__(self):
        self.create_brazier = random.choice([
            self.unlit,
            self.smouldering,
            self.burning,
            self.intensely_burning])

    def apply_to(self, room):
        brazier, aura = self.create_brazier()
        brazier.material = random.choice(self.materials)
        brazier.location = self.random_wall(room)
        if aura is not None:
            room.initiate_aura(aura)
        room.add(brazier)

    def unlit(self):
        deco = Decoration(['unlit brazier', 'bowl on stilts'])
        deco.BriefDescription = 'a brazier to the {location}'
        return deco, None

    def smouldering(self):
        deco = Decoration(['smouldering brazier', 'smoldering brazier', 'bowl on stilts'])
        self.AuraDescription = 'A dim light slightly illuminates this room from {relative_direction}'
        deco.BriefDescription = 'a brazier to the {location}'
        return deco, self.start_aura(2, 0.2)

    def burning(self):
        deco = Decoration(['burning brazier','bowl on stilts'])
        self.AuraDescription = 'A golden, flickering light dances on the walls from {relative_direction}'
        deco.BriefDescription = 'a brazier to the {location}'
        return deco, self.start_aura(4, 0.5)

    def intensely_burning(self):
        deco = Decoration(['burning brazier','bowl on stilts'])
        self.AuraDescription = 'An intense, golden, flickering light erupts from {relative_direction}'
        deco.BriefDescription = 'a brazier to the {location}'
        return deco, self.start_aura(6, 0.6)

    def start_aura(self, strength, decay):
        self.light_power = strength
        aura = Aura(None, strength, decay)
        aura.blocked_by_walls = True
        aura.modify_light = self.modify_light
        aura.BriefDescription = self.AuraDescription
        return aura

    def modify_light(self, decay=1):
        return self.light_power * decay
