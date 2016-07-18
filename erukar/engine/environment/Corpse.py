from erukar.engine.environment.Decoration import Decoration

class Corpse(Decoration):
    def __init__(self, lifeform):
        aliases = [lifeform.alias() + ' corpse']
        description = 'On the ground is a corpse of a {}'.format(lifeform.alias())
        inspect = 'The {} appears to have been killed recently.'.format(lifeform.alias())
        super().__init__(aliases,description,inspect)
