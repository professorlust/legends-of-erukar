from erukar.engine.environment.Decoration import Decoration

class Corpse(Decoration):
    def __init__(self, lifeform):
        self.lifeform_alias = lifeform.alias()
        aliases = [self.lifeform_alias + ' corpse']
        super().__init__(aliases)
        self.set_vision_results('','You see the corpse of a {lifeform_alias}',(3,3))
        self.set_sensory_results('You smell death nearby.', 'You smell the corpse of a {lifeform_alias}', (0,5))
        self.set_detailed_results('In this room is a corpse.', 'The corpse of a {lifeform_alias} lies on the floor. It has been killed recently.')
