from erukar.engine.environment.Container import Container

class Corpse(Container):
    def __init__(self, lifeform):
        self.lifeform_alias = lifeform.alias()
        aliases = [self.lifeform_alias + ' corpse']
        super().__init__(aliases)
        self.can_close = False
        self.contents = lifeform.inventory
        self.contents_visible = True
