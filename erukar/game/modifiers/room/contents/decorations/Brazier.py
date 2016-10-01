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
        deco.set_vision_results('You see a bowl standing on stilts to {location} of the room.',\
                                'You see an unlit {material} brazier to the {location}',\
                                (1, 20))
        deco.set_sensory_results('','',(0,0))
        deco.set_detailed_results('You see a bowl standing on stilts to the {location} of the room.',\
                                'You see an unlit {material} brazier to the {location}')
        return deco, None

    def smouldering(self):
        deco = Decoration(['smouldering brazier', 'smoldering brazier', 'bowl on stilts'])
        self.AuraDescription = 'A dim light slightly illuminates this room from {relative_dir}'
        deco.BriefDescription = 'a brazier to the {location}'
        deco.set_vision_results('You see a bowl standing on stilts to the {location} of the room.',\
                                'You see a {material} brazier to the {location}',\
                                (1, 20))
        deco.set_sensory_results('You feel the air around you raise in temperature slightly.',
                                 'The room\'s temperature fluctuates slightly, as if there were an open source of flames somewhere in the room.',(2,15))
        deco.set_detailed_results('You see a bowl standing on stilts to the {location} of the room; there are small flames and glowing embers inside of the bowl, and the temperature of the room seems to be higher because of the flames.',\
                                'You see a brazier to the {location}. Small flames and glowing embers sit inside of the bowl, casting flickering yet faint light across the room. You feel slightly warmer due to the heat from the flames.')
        return deco, self.start_aura(2, 0.2)

    def burning(self):
        deco = Decoration(['burning brazier','bowl on stilts'])
        self.AuraDescription = 'A golden, flickering light dances on the walls from {relative_direction}'
        deco.BriefDescription = 'a brazier to the {location}'
        deco.set_vision_results('You see a bowl standing on stilts to the {location} of the room.',\
                                'You see a {material} brazier to the {location}',\
                                (1, 20))
        deco.set_sensory_results('The room seems warmer.',\
                                 'The room\'s temperature rises and you feel the warmth of flames from a brazier to the {direction}.',\
                                 (5,30))
        deco.set_detailed_results('A bowl of warm flames casts light across the room from the {location}.',
                                'You see a brazier to the {location}. A gentle, yet lively fire is burning from embers and other fuel inside of the bowl, warming the room and casting light all around the room.')
        return deco, self.start_aura(4, 0.5)

    def intensely_burning(self):
        deco = Decoration(['burning brazier','bowl on stilts'])
        self.AuraDescription = 'An intense, golden, flickering light erupts from {relative_direction}'
        deco.BriefDescription = 'a brazier to the {location}'
        deco.set_vision_results('You see a bowl standing on stilts to the {location} of the room.',\
                                'You see a {material} brazier to the {location}',\
                                (1, 20))
        deco.set_sensory_results('The room seems very warm.',\
                                 'The room\'s temperature rises and you feel a great warmth of flames from a brazier to the {direction}.',\
                                 (5,30))
        deco.set_detailed_results('A bowl of intensely hot flames casts bright light across the room from the {location}.',
                                'You see a brazier to the {location}. An out of control fire erupts from the bowl, heating the rest of the room intensely and unsettling you just slightly.')
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
