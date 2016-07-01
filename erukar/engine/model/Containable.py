from erukar.engine.model.RpgEntity import RpgEntity
from erukar.engine.model.EnvironmentPiece import EnvironmentPiece

class Containable(EnvironmentPiece):
    def __init__(self, aliases, broad_results, inspect_results):
        super().__init__(aliases, broad_results, inspect_results)
        self.contents = []
        self.contents_conjuntion = " Inside of the container:  "

    def add(self, item):
        self.contents.append(item)

    def on_inspect(self):
        descriptions = ' '.join([c.describe() for c in self.contents if c.describe() is not None])
        if len(self.contents) > 0:
            return self.inspect_results + self.contents_conjuntion + descriptions
        return self.inspect_results

    def remove(self, entity):
        target = next((x for x in self.contents if x == entity), None)
        self.contents.remove(target)
