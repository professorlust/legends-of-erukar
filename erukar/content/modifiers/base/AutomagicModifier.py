from .ItemModifier import ItemModifier
from erukar.system.engine import SpellInstance
import erukar


class AutomagicModifier(ItemModifier):
    def get_effects(self):
        return [
            erukar.content.PotionSource,
            erukar.content.AddHealth
        ]

    def tick(self, cmd, owner):
        effects = self.get_effects()
        spell = SpellInstance(effects)
        spell.cmd_execute(cmd, caster=owner)
