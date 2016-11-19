from erukar.engine.commands.Command import Command
from erukar.engine.model.Damage import Damage
from erukar.engine.lifeforms import Lifeform

class Stats(Command):
    status = 'Health:    {} / {}\nEvasion:   {}'
    level = 'Level:     {}\nXP:        {} / {}'
    stat = "{0:10} {1}"
    attribute_types = [
        "strength",
        "dexterity",
        "vitality",
        "acuity",
        "sense",
        "resolve"]
    descriptions = {
        "strength": "A measure of brawn and physical power. A higher score allows you to deal more physical damage and exert more force on the world.",
        "dexterity": "A measure of speed, reflexes, and overall finesse. A higher score allows you to evade attacks with greater ease, move faster than your opponents, and hit your opponents with specific dextrous attacks.",
        "vitality": "A measure of physical fitness and fortitude. The higher your vitality score is, the more overall health you have and the more rapidly you can recover it.",
        "acuity": "A measure of mental intellect, investigative prowess, and visual observation capacity. The higher this score is, the more damage you can deal with arcane magics and the better you can visually perceive the world around you.",
        "sense": "A measure of gut instincts, common sense, and basic senses like smell and thermoreception. Your ability to intuitively judge the scenarios and situation of the world around you is governed by this ability score.",
        "resolve": "A measure of mental fortitude and resilience. The higher your score is, the more likely you are to overcome afflictions and highly dangerous situations."
    }

    aliases = ['stats', 'attributes', 'vitals']

    def execute(self, *_):
        self.check_for_arguments()

        status_d = self.status.format(
            self.lifeform.health, 
            self.lifeform.max_health,
            self.lifeform.calculate_armor_class())

        level_d = self.level.format(
            self.lifeform.level, 
            self.lifeform.experience, 
            self.lifeform.calculate_necessary_xp())

        attribute_d = '\n'.join([Stats.stat.format(
                stat.capitalize(), 
                self.lifeform.calculate_stat_score(stat))
            for stat in self.attribute_types])

        mitigations = '\n'.join(['{:12} {:3}% MIT / {:2} DFL'.format(
            dtype.capitalize(),
            int(100.0*(1-self.lifeform.mitigation(dtype))), self.lifeform.deflection(dtype))
            for dtype in Damage.Types])

        self.append_result(self.sender_uid, '\n--------------------\n'.join([level_d, status_d, attribute_d, mitigations]))

        return self.succeed()

    def give_details(self, wanted, lifeform):
        desc = self.descriptions[wanted]
        result = ['{}: {}'.format(wanted.capitalize(), desc),\
                'Your current {} score:  {}'.format(wanted, lifeform.calculate_stat_score(wanted))]
        return '\n\n'.join(result)
