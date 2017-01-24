from erukar.engine.environment.Door import Door

class InstanceTransition(Door):
    def on_open(self, opener):
        opener.transition_properties = self.get_transition_properties()
        self.status = Door.Closed
        return super().on_open(opener)

    def get_transition_properties(self):
        return None
