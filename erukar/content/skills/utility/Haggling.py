from erukar.system.engine import Skill

class Haggling(Skill):
    Name = 'Haggling'

    def current_level_description(self):
        return 'Reduces vendor prices by anywhere from {}% to {}%'.format(Haggling.lower_at(self.level), Haggling.upper_at(self.level))

    def next_level_description(self):
        lower = Haggling.lower_at(self.level+1)
        upper = Haggling.upper_at(self.level+1)
        return 'Further decreases vendor prices ({}% to {}%)'.format(lower, upper)

    def lower_at(self, level):
        if level <= 3:
            return 0.5 + 2 * level # 2.5, 4.5, 6.5
        if level < 6:
            return 5.5 + 0.5*level # 7.5, 8.0
        return 6.25 + 0.25*level # 8.25, 8.5, 8.75

    def upper_at(self, level):
        if level <= 3:
            return 3.0 * level # 3.0, 6.0, 9.0
        if level < 6:
            return 4.5 + 1.5 * level # 10.5, 12.0
        return 10.5 + 0.75 * level # 12.75, 13.5, 14.5

    def apply_to(self, skilled):
        skilled.haggling_range = self.haggling_range

    def haggling_range(self):
        return (Haggling.lower_at(self.level), Haggling.upper_at(self.level))

