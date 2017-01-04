class ScriptPayload:
    def __init__(self, shard_interface, uid, playernode, character, user_input):
        self.interface = shard_interface
        self.playernode = playernode
        self.uid = uid
        if playernode and not character:
            self.character = playernode.character
        else: self.character = character
        self.user_input = user_input
