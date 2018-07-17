from erukar.system.engine import MagicEffect


class Cryomorph(MagicEffect):
    def enact(self, instigator, target, cmd, mutator):
        mutator.set('damage_type', 'ice')
        return mutator
