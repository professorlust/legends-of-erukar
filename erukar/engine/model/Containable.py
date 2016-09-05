from erukar.engine.model.RpgEntity import RpgEntity
from erukar.engine.model.EnvironmentPiece import EnvironmentPiece

class Containable(EnvironmentPiece):
    def __init__(self, aliases):
        super().__init__(aliases)
        self.contents = []
        self.contents_conjuntion = " Inside of the container:  "
        
    def add(self, item):
        self.contents.append(item)

    def on_inspect(self, player=None):
        descriptions = ' '.join(list(self.inspect_gen(player)))
        if len(self.contents) > 0:
            return self.inspect_results + self.contents_conjuntion + descriptions
        return self.inspect_results

    def inspect_gen(self, player):
        for c in self.contents:
            if c is not player:
                res = c.describe()
                if res is not None:
                    yield res

    def remove(self, entity):
        target = next((x for x in self.contents if x == entity), None)
        self.contents.remove(target)
