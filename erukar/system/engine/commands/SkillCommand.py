from .ActionCommand import ActionCommand

class SkillCommand(ActionCommand):
    GoverningSkill = None

    @classmethod
    def can_use(cls, for_player):
        return any(isinstance(skill, cls.GoverningSkill) for skill in for_player.skills)

    def should_appear_at(x, y):
        return False

    def should_appear_for(obj):
        return False

    def should_appear_in_list():
        return False
