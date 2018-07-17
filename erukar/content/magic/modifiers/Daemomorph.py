from erukar.system.engine import MagicEffect


class Daemomorph(MagicEffect):
    def enact(self, instigator, target, cmd, mutator):
        mutator.set('damage_type', 'demonic')
        mutator.set('sanctity', -1)
        return mutator
