from erukar.system.engine import Skill


class ImprovedSight(Skill):
    Name = 'Improved Self Awareness'

    def current_level_description(self):
        return 'Improves radius on vision by {}'.format(self.radius())

    def next_level_description(self):
        return 'Adds 0.5 to vision radius (totalling +{})'.format(self.radius()+0.5)

    def radius(self):
        return 1 + 0.5*self.level

    def apply_to(self, skilled):
        skilled.visual_fog_of_war = self.visual_fog_of_war

    def visual_fog_of_war(self):
        return self.radius() + 4.0
