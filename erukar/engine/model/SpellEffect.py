from erukar.engine.model.MagicBase import MagicBase
from erukar.engine.model.Damage import Damage

class SpellEffect(MagicBase):
    def inflict_damage(instigator, enemy, damage):
        for deflected in Damage.deflections(instigator, enemy, None,):
            self.append_result(instigator.sender_uid, Attack.deflected.format(**args))
            self.append_result(enemy.uid, Attack.deflected.format(**args))

        actuals = list(Damage.actual_damage_values(instigator, enemy, None, damages))
        xp = enemy.take_damage(damage, instigator)

