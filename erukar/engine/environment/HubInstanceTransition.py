from .InstanceTransition import InstanceTransition
from erukar.engine.model.TransitionState import TransitionState

class HubInstanceTransition(InstanceTransition):
    def __init__(self, description, new_instance_id, coordinates):
        super().__init__(description)
        self.instance_id = new_instance_id
        self.coordinates = coordinates

    def get_transition_properties(self):
        return TransitionState.hub(self.instance_id, self.coordinates)
