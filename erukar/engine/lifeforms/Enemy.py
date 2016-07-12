from erukar.engine.lifeforms.Lifeform import Lifeform

class Enemy(Lifeform):
    def perform_turn(self):
        print('{} is performing a turn'.format(self.name))
