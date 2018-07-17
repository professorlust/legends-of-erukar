from erukar.system.engine import MagicEffect


class Arcanomorph(MagicEffect):
    def enact(self, instigator, target, cmd, mutator):
        mutator.set('damage_type', 'arcane')
        return mutator
