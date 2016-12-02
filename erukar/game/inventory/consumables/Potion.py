from erukar.engine.inventory.StackableItem import StackableItem
import erukar

class Potion(StackableItem):
    Persistent = True
    BaseName = "Potion"
    BriefDescription = "a red potion"

    def __init__(self, quantity=1):
        super().__init__(self.BaseName, quantity)
        self.effect = erukar.game.magic.effects.HealEffect()

    def on_use(self, cmd, target):
        self.effect.on_cast(cmd, target)
        self.consume()
        return '', True
