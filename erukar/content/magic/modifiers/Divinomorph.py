from erukar.system.engine import MagicEffect


class Divinomorph(MagicEffect):
    def enact(self, instigator, target, cmd, mutator):
        mutator.set('damage_type', 'divine')
        mutator.set('sanctity', 1)
        return mutator
