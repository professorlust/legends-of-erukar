from erukar.engine.environment.Door import Door

class InstanceTransition(Door):
    def __init__(self, description, new_instance_id):
        super().__init__(description)
        self.instance_id = new_instance_id

    def on_open(self, opener):
        opener.instance = self.instance_id
        self.status = Door.Closed
        return super().on_open(opener)
