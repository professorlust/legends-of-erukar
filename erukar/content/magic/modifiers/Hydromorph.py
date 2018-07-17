from erukar.system.engine import MagicEffect


class Hydromorph(MagicEffect):
    def enact(self, instigator, target, cmd, mutator):
        mutator.set('damage_type', 'aqueous')
        return mutator
