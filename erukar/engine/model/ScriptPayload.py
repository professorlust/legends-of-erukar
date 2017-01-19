class ScriptPayload:
    def __init__(self, shard, uid, playernode, character, user_input):
        self.shard = shard
        self.interface = shard.interface
        self.playernode = playernode
        self.uid = uid
        if playernode and not character:
            self.character = playernode.character
        else: self.character = character
        self.user_input = user_input
