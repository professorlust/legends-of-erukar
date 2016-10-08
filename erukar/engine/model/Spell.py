from erukar.engine.model.Describable import Describable

class Spell(Describable):
    def __init__(self, name, description, effect_strategem):
        self.name = name
        self.description = description
        self.effects = effect_strategem

    def on_cast(self, lifeform, efficacy=1.0):
        self.lifeform = lifeform
        return '\n\n'.join([self.mutate(self.description)] + [eff.on_cast(lifeform, efficacy) for eff in self.effects])
