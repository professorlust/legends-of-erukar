from erukar.engine.model.RpgEntity import RpgEntity
import random

class EnvironmentPiece(RpgEntity):
    def __init__(self, aliases):
        super().__init__()
        self.aliases = aliases

    def matches(self, query):
        return any([query in alias for alias in self.aliases])

    def alias(self):
        return random.choice(self.aliases)

    def describe(self):
        return self.description

    def get_name(self):
        return random.choice(self.aliases)
