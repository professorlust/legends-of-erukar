from erukar.system.engine import SkillCommand
import erukar

class OverwhelmCommand(SkillCommand):
    GoverningSkill = erukar.content.skills.Overwhelm

    def should_appear_in_list():
        return True

    def should_appear_at(x, y):
        return False

    def should_appear_for(obj):
        return False
