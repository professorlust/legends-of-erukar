from erukar.system.engine import StackableItem, SpellInstance
from erukar.ext.nlg import Drink


class Potion(StackableItem):
    Persistent = True
    BaseName = "Potion"
    IsUsable = True
    BriefDescription = "a red potion"

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
