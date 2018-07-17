from erukar.system.engine import MagicEffect


class Pyromorph(MagicEffect):
    def enact(self, instigator, target, cmd, mutator):
        mutator.set('damage_type', 'fire')
        return mutator
