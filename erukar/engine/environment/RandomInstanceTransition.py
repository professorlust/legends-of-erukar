from .InstanceTransition import InstanceTransition
from erukar.engine.model.TransitionState import TransitionState

class RandomInstanceTransition(InstanceTransition):
    def __init__(self, description, generation_properties):
        super().__init__(description)
        self.generation_properties = generation_properties

    def get_transition_properties(self):
        return TransitionState.random(self.generation_properties)

