from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class GrassyFloor(RoomModifier):
    Proability = 2.0
    ProbabilityFromFabrication = -0.8

    healths = [
        ('tall grass', 'Tall grass rises from the ground.', 'Tall stalks of grass rise up to just below your knees, making it hard to see the surface.'),
        ('dirt with several bunches of young grass seedlings', 'The dirt floor has some distinct grass seedlings growing out of it.', 'New grass seedlings, maybe several days since planted, are starting to grow out of the rough clay earth below your feet.'),
        ('recently cut grass', 'This grass seems to have been cut recently.', 'The grass rises about a centimeter out of the ground and the smell of freshly cut grass fills the room.'),
        ('short grass', 'The grass is short.', 'The grass rises several inches out of the earth, just below your ankles.'),
        ('dead grass', 'Dying grass rises and droops back to the ground.', 'Yellowing grass rises from the earth below you, but droops back to the ground. There is no resurrection for this grass.')
    ]
    fields = ['health']

    def apply_to(self, room):
        room.floor = Surface('The floor is covered in grass.')
        room.floor.BriefDescription = self.health[0]
        # Don't worry about setting vision or sensory results because detailed should always be used
        room.floor.set_vision_results("","", (1, 35))
        room.floor.set_sensory_results("","", (0,0))
        room.floor.set_detailed_results(self.health[1], self.health[2])
