from erukar.system.engine import FactoryBase
from ..Command import Command

import logging
logger = logging.getLogger('debug')

class AddSkill(Command):
    RebuildZonesOnSuccess = True

    '''
    Requires
        skill
    '''

    def perform(self):
        if self.invalid('skill'): return self.fail('Skill is invalid')

        if self.args['player_lifeform'].skill_points <= 0:
            return self.fail('Not enough skill points to acquire a new skill')

        skill = FactoryBase.create_one(self.args['skill'])
        if not skill: return self.fail('Could not find skill')

        if any([isinstance(sk, type(skill)) for sk in self.args['player_lifeform'].skills]):
            return self.fail('Duplicate Skill found.')

        self.dirty(self.args['player_lifeform'])
        self.args['player_lifeform'].add_skill(skill)
        return self.succeed()
