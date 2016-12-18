from erukar.engine.model.Condition import Condition
import erukar

class Disoriented(Condition):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    def __init__(self, target):
        super().__init__(target)
        self.timer = self.Duration
        self.base_acuity = self.target.acuity
        self.target.acuity = int(self.target.acuity/2)

    def tick(self):
        if self.IsTemporary:
            self.timer -= 1
            if self.timer <= 0:
                self.exit()

    def exit(self):
        self.target.acuity = self.base_acuity
        self.target.conditions.remove(self)
