from erukar.system.engine import SkillCommand
import erukar

class HideCommand(SkillCommand):
    GoverningSkill = erukar.content.skills.Hide

    def should_appear_in_list():
        return True

