from erukar.system.engine import Skill

class Charisma(Skill):
    Name = 'Charisma'

    def current_level_description(self):
        return 'Improves NPC disposition by {}%'.format(self.bonus())

    def next_level_description(self):
        return 'Increases NPC disposition bonuses by {}%'.format(self.bonus()+1.0)

    def bonus(self):
        return 5.0 + self.level

    def apply_to(self, skilled):
        skilled.disposition_bonuses = self.disposition_bonuses
