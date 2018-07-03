from erukar.system.engine import Enemy
from erukar.content.inventory import Claws


class MalformedDemon(Enemy):
    BriefDescription = "a malformed demon"
    Probability = 1
    ClassName = "Malformed Demon"
    ClassLevel = 2

    def init_stats(self):
        self.dexterity = 1
        self.vitality = 0
        self.strength = 0
        self.resolve = 2
        self.sense = 2
        self.acuity = 1

    def init_inventory(self):
        self.left = Claws()
        self.right = Claws()
        self.inventory = [self.left, self.right]
