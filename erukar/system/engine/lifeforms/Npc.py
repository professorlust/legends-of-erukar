from .Lifeform import Lifeform

class Npc(Lifeform):
    def __init__(self, templates=[]):
        super().__init__()
        self.qualities = []
        for template in templates:
            template.apply(self)
