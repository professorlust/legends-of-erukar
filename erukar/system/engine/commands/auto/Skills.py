import erukar
from erukar.system.engine import Lifeform
from ..Command import Command

class Skills(Command):
    NeedsArgs = False

    def perform(self):
        available = [Skills.format(skill) for skill in self.unacquired_skills()]
        acquired = [Skills.format(skill) for skill in self.args['player_lifeform'].skills]
        full_list = {
            'available': available,
            'acquired': acquired
        }
        self.append_result(self.player_info.uid, full_list)
        return self.succeed()

    def format(skill):
        return {
            'name': skill.Name,
            'level': skill.level,
            'maxLevel': 8,
            'description': skill.current_level_description(),
            'nextLevelDescription': skill.next_level_description(),
            'type': skill.__module__
        }

    def unacquired_skills(self):
        for skill in Skills.all_possible():
            if not any(isinstance(acquired, skill) for acquired in self.args['player_lifeform'].skills):
                yield skill()

    def all_possible():
        return [
            erukar.content.skills.ArcaneGift,
            erukar.content.skills.ArcaneTraining,
            erukar.content.skills.Bloodlust,
            erukar.content.skills.Rage,
            erukar.content.skills.ImprovedSight,
            erukar.content.skills.MartialWeaponTraining,
            erukar.content.skills.PolearmTraining,
            erukar.content.skills.BowTraining,
            erukar.content.skills.CrossbowTraining
        ]
