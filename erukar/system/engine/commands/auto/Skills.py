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
        player = self.args['player_lifeform']
        for skill in Skills.all_possible():
            if player.has_skill(skill):
                continue
            if skill.meets_requirements(player):
                yield skill()

    def all_possible():
        return [
            erukar.content.skills.ArcaneGift,
            # erukar.content.skills.BloodMagic
            erukar.content.skills.PracticedSpellcasting,
            # erukar.content.skills.SpellDeflection()
            erukar.content.skills.WandTraining,
            # erukar.content.skills.CleanseDesecrate,
            erukar.content.skills.Heal,
            # erukar.content.skills.Prayer,
            erukar.content.skills.Smite,
            erukar.content.skills.SupernaturalSense,
            erukar.content.skills.MartialWeaponTraining,
            erukar.content.skills.Cleave,
            erukar.content.skills.Lunge,
            # erukar.content.skills.BasicStances,
            # erukar.content.skills.ArmorTraining,
            erukar.content.skills.Defend,
            # erukar.content.skills.Intuition,
            # erukar.content.skills.KnowYourEnemy,
            # erukar.content.skills.Parry,
            # erukar.content.skills.Rally,
            erukar.content.skills.Dodge,
            erukar.content.skills.EagleEye,
            erukar.content.skills.Hide,
            # erukar.content.skills.RangedWeaponTraining,
            # erukar.content.skills.Sprint,
        ]

    def all_activatable(self):
        player = self.args['player_lifeform']
        for skill in player.skills:
            if isinstance(skill, SidebarAbility):
                yield Skills.format_active(skill)
