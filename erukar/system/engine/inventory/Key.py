from .StackableItem import StackableItem
import random

class Key(StackableItem):
    Persistent = False
    BriefDescription = "a key"
    BaseName = "Key"
    SuccessfulUnlock = 'You have successfully unlocked the {target}.'
    FailedToUnlock = 'You have failed to unlock the {target}.'

    def on_use(self, command, target):
        cmd.append_result(cmd.sender_uid, self.mutate(self.FailedToUnlock,{'target': target.alias()}))
        return False
