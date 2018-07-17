from erukar.system.engine import MagicEffect


class Kinetomorph(MagicEffect):
    def enact(self, instigator, target, cmd, mutator):
        mutator.set('damage_type', 'force')
        return mutator
