from .EnvironmentPiece import EnvironmentPiece

class Containable(EnvironmentPiece):
    def __init__(self, aliases):
        super().__init__(aliases)
        self.contents = []
        self.contents_conjuntion = "Inside of the container:  "

    def get_object_by_uuid(self, uuid):
        if uuid == self.uuid: 
            yield self
            raise StopIteration

        for obj in self.contents:
            if obj.uuid and obj.uuid == uuid:
                yield obj
            if isinstance(obj, Containable):
                for sub_obj in obj.get_object_by_uuid(uuid):
                    yield sub_obj

    def add(self, item):
        self.contents.append(item)

    def on_inspect(self, player, acuity, sense):
        descriptions = ', '.join(list(self.inspect_gen(player)))
        if len(self.contents) > 0:
            return self.contents_conjuntion + descriptions
        return descriptions

    def inspect_gen(self, player):
        for c in self.contents:
            if c is not player and (hasattr(c, 'IsInteractible') and c.IsInteractible):
                res = c.describe()
                if res is not None:
                    yield res

    def remove(self, entity):
        target = next((x for x in self.contents if x == entity), None)
        self.contents.remove(target)
