from erukar.system.engine import Describable

class Surface(Describable):
    def __init__(self, description="This is a wall."):
        super().__init__()
        self.description = description

    def inspect_through(self, *_):
        return self.describe()
