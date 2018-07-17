from .StackableItem import StackableItem
import random

class Key(StackableItem):
    Persistent = False
    BriefDescription = "a key"
    BaseName = "Key"
    SuccessfulUnlock = 'You have successfully unlocked the {target}.'
    FailedToUnlock = 'You have failed to unlock the {target}.'

    def alias(self):
        self.name = 'Key'
        return super().alias()

    def on_use(self, command, target):
        return False
