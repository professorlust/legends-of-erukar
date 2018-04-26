from erukar.system.engine import Skill

class EconomicSense(Skill):
    Name = 'Economic Sense'

    def current_level_description(self):
        return 'Allows insight into NPC prices, showing what goods are high in supply or demand. Higher skill levels reveal less clear-cut definitions.'

    def next_level_description(self):
        return 'Improves ability to determine more difficult economics' 

    def apply_to(self, skilled):
        pass
