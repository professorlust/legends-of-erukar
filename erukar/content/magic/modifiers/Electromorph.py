from erukar.system.engine import MagicEffect


class Electromorph(MagicEffect):
    def enact(self, instigator, target, cmd, mutator):
        mutator.set('damage_type', 'electric')
        return mutator
