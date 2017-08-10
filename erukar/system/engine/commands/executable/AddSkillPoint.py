from erukar.system.engine import FactoryBase
from ..Command import Command

class AddSkillPoint(Command):
    RebuildZonesOnSuccess = True

    '''
    Requires
        skill
    '''

    def perform(self):
        if self.invalid('skill'): return self.fail('Skill is invalid')

        if self.args['player_lifeform'].skill_points <= 0:
            return self.fail('Not enough skill points to level a skill')

        module, skill_type = FactoryBase.module_and_type(self.args['skill'])
        if not skill_type: return self.fail('Type of Skill is invalid')

        skill = next((sk for sk in self.args['player_lifeform'].skills if isinstance(sk, getattr(module, skill_type))), None)
        if not skill:
            return self.fail('Cannot find skill to add point')

        self.dirty(self.args['player_lifeform'])
        skill.level += 1
        self.args['player_lifeform'].skill_points -= 1
        return self.succeed()
