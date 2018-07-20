from erukar.system.engine import Skill

class Haggling(Skill):
    Name = 'Haggling'

    def current_level_description(self):
        reduction = Haggling.reduction(self.level)
        return 'Reduces vendor prices by {}%'.format(reduction)

    def next_level_description(self):
        reduction = Haggling.reduction(self.level+1)
        return 'Further decreases vendor prices (to {}% reduction)'.format(reduction)

    def reduction(level):
        if level <= 3:
            return 0.5 + 2 * level # 2.5, 4.5, 6.5
        if level < 6:
            return 5.5 + 0.5*level # 7.5, 8.0
        return 6.25 + 0.25*level # 8.25, 8.5, 8.75

    def apply_to(self, skilled):
        skilled.haggling_sell_modifier = self.haggling_sell_modifier
        skilled.haggling_buy_modifier = self.haggling_buy_modifier

    def haggling_sell_modifier(self):
        return 1.2 - (0.01 * Haggling.reduction(self.level))

    def haggling_buy_modifier(self):
        return 0.8 + (0.01 * Haggling.reduction(self.level))
