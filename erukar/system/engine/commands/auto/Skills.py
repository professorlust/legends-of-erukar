import erukar
from erukar.system.engine import Lifeform, SidebarAbility
from ..Command import Command


class Skills(Command):
    NeedsArgs = False

    def perform(self):
        available = [Skills.format(skill) for skill in self.unacquired_skills()]
        acquired = [Skills.format(skill) for skill in self.acquired_skills()]
        activatable = list(self.all_activatable())
        full_list = {
            'skillPoints': self.args['player_lifeform'].skill_points,
            'available': available,
            'acquired': acquired,
            'activatable': activatable
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

    def format_active(skill):
        return {
            'name': skill.Name,
            'abbreviation': skill.ActiveAbbreviation,
            'abilityModule': skill.__module__
        }

    def acquired_skills(self):
        for skill in self.args['player_lifeform'].skills:
            if skill.ShowInLists:
                yield skill

    def unacquired_skills(self):
        for skill in Skills.all_possible():
            if not any(isinstance(acquired, skill) for acquired in self.args['player_lifeform'].skills):
                yield skill()

    def all_possible():
        return [
            erukar.content.skills.ArcaneGift,
            erukar.content.skills.ArcaneTraining,
            erukar.content.skills.BowTraining,
            erukar.content.skills.Charisma,
            erukar.content.skills.CrossbowTraining,
            erukar.content.skills.EconomicSense,
            erukar.content.skills.Haggling,
            erukar.content.skills.ImprovedSight,
            erukar.content.skills.MartialWeaponTraining,
            erukar.content.skills.PolearmTraining,
            erukar.content.skills.Smite,
            erukar.content.skills.Cleave,
            erukar.content.skills.Rage,
            erukar.content.skills.Heal,
            erukar.content.skills.Defend,
            erukar.content.skills.Dodge,
            erukar.content.skills.Lunge
        ]

    def all_activatable(self):
        player = self.args['player_lifeform']
        for skill in player.skills:
            if isinstance(skill, SidebarAbility):
                yield Skills.format_active(skill)
