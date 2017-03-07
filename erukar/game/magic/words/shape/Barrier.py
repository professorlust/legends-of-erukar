from erukar.engine.magic.SpellWord import SpellWord
import erukar

class Barrier(SpellWord):
    TargetResult = 'A barrier appears around you!' 
    ViewerResult = 'A barrier appears around {alias|target}!'

    DamageType = 'force'

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        super().on_cast(command, lifeform, parameters, efficacy)

        barrier = erukar.game.conditions.positive.Shielded(self.target)
        barrier.damage_type = self.DamageType
        barrier.set_efficacy(efficacy)

        if self.caster.uid != self.target.uid:
            self.append_result(self.caster.uid, self.mutate(self.ViewerResult))

        self.append_for_others_in_room(self.mutate(self.ViewerResult))
        self.append_result(self.target.uid, self.mutate(self.TargetResult))
        
        self.target.conditions.append(barrier)
