from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class DirtFloor(RoomModifier):
    Proability = 2.0
    ProbabilityFromFabrication = -0.8

    depths = [
        ('stone covered in dirt', 'You are standing on a dirty stone floor.', 'A thin layer of dirt covers a stone floor.'),
        ('uneven ground','The ground is unlevel dirt.','The ground is made of a mixture of unlevel dirt mounds and stones.'),
        ('dry dirt', 'You are standing on a section of very dry dirt.','Rough, sparse patches of dead grass and weeds permeate the earth below your feet.')
    ]

    fields = ['depth']

    def apply_to(self, room):
        args = self.get_arguments()
        room.floor = Surface("")
        room.floor.BriefDescription = self.depth[0]
        # Don't worry about setting vision or sensory results because detailed should always be used
        room.floor.set_vision_results("","", (1, 35))
        room.floor.set_sensory_results("","", (0,0))
        room.floor.set_detailed_results(self.depth[1], self.depth[2])
