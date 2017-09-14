from erukar.system.engine import StackableItem
from erukar.ext.nlg import Drink
import erukar

class Potion(StackableItem):
    Persistent = True
    BaseName = "Potion"
    IsUsable = True
    BriefDescription = "a red potion"

    def __init__(self, quantity=1):
        super().__init__(self.BaseName, quantity)
        self.source = None
        self.effect = None

    def alias(self):
        return 'Potion x{}'.format(self.quantity)

    def price(self):
        return 10

    def on_use(self, observer):
        observer.health = min(observer.max_health, observer.health + 10)
        self.consume()
        return Drink.taste(observer, *observer.get_detection_pair(), self)

    def duplication_args(self, quantity):
        return {
            'quantity': quantity,
        }
