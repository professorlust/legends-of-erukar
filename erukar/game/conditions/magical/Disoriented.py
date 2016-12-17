from erukar.engine.model.Affliction import Affliction
import erukar

class Disoriented(Affliction):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    def __init__(self, afflicted):
        super().__init__(afflicted)
        self.timer = self.Duration
        self.base_acuity = self.afflicted.acuity
        self.afflicted.acuity = int(self.afflicted.acuity/2)

    def tick(self):
        if self.IsTemporary:
            self.timer -= 1
            if self.timer <= 0:
                self.exit()

    def exit(self):
        self.afflicted.acuity = self.base_acuity
        self.afflicted.afflictions.remove(self)
