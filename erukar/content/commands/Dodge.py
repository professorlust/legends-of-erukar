from erukar.system.engine import SkillCommand
import erukar

class DodgeCommand(SkillCommand):
    GoverningSkill = erukar.content.skills.Dodge

    def should_appear_in_list():
        return True
