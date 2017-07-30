from erukar.system.engine import Describable

class Wall(Describable):
    def __init__(self):
        super().__init__()
        self.material = None
