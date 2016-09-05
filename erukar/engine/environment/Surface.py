from erukar.engine.model.RpgEntity import RpgEntity

class Surface(RpgEntity):
    def __init__(self, description="This is a wall."):
        self.description = description

    def describe(self, *_):
        return self.description

    def inspect_through(self, *_):
        return self.describe()
