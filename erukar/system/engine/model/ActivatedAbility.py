from .Skill import Skill


class ActivatedAbility(Skill):
    ActiveAbbreviation = 'NONE'

    def perform(self, cmd):
        pass

    def can_activate(self):
        return False
