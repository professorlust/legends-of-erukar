from erukar.engine.model.MagicBase import MagicBase

class Spell(MagicBase):
    YouCastSpell = "You cast '{name}'."
    TheyCastSpell = "{alias|lifeform} casts '{name}'."

    def __init__(self, name, effect_strategem):
        self.name = name
        self.effects = effect_strategem

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        super().on_cast(command, lifeform, parameters, efficacy)

        self.append_result(lifeform.uid, self.mutate(self.YouCastSpell))
        self.append_for_others_in_room(self.mutate(self.TheyCastSpell))

        for eff in self.effects:
            parameters = eff.on_cast(command, self.target, parameters, efficacy)

    def alias(self):
        return self.name
