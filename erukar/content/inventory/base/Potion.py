from erukar.system.engine import StackableItem, SpellInstance
from erukar.ext.nlg import Drink


class Potion(StackableItem):
    Persistent = True
    BaseName = "Potion"
    IsUsable = True
    BriefDescription = "a red potion"
    Basic = 'A small vial, perhaps 50 mL in volume, filled '\
        'with some sort of red liquid.'
    BadSense = 'It smells like a potion of some sort.'
    GoodSense = 'Smelling the contents, you get hints of rose '\
        'petals and cinnamon.'
    BadVision = 'The liquid sloshes around in the vial as you '\
        'shake it.'
    GoodVision = 'The liquid inside the potion glimmers with '\
        'faint golden sparkles when held against light.'
    Effect = 'This potion actually has no effect.'

    def __init__(self, quantity=1):
        super().__init__(self.BaseName, quantity)
        self.effects = []

    def duplication_args(self, quantity):
        return {
            'quantity': quantity,
        }

    def price(self, econ=None):
        return 10

    def on_use(self, cmd):
        self.consume(cmd)
        observer = cmd.args['player_lifeform']
        acu, sen = observer.get_detection_pair()
        cmd.args['kwargs'] = self.get_kwargs()
        cmd.append_result(observer.uid, Drink.taste(observer, acu, sen, self))
        spell = SpellInstance(self.effects)
        spell.cmd_execute(cmd)
        return cmd.succeed()

    def get_kwargs(self):
        return {}

    def flavor_text(self, player):
        return ' '.join([
            self.Basic,
            (self.GoodSense if player.sense >= 10 else self.BadSense),
            (self.GoodVision if player.acuity >= 10 else self.BadVision),
            self.Effect])
