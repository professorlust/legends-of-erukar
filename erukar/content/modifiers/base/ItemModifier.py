from erukar.system.engine import Modifier, Item, SpellInstance


class ItemModifier(Modifier):
    PermittedEntities = []

    def apply_to(self, item):
        super().apply_to(item)
        item.modifiers.append(self)

    def execute_magic_chain(self, chain, instigator, target, **kwargs):
        spell = SpellInstance(chain)
        log = spell.execute(instigator, target, **kwargs)
        return log
