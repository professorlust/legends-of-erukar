from erukar.server.Instance import Instance

class HubInstance(Instance):
    def __init__(self, file_path):
        self.hub_definition_file_path = file_path
        super().__init__()

    def initialize_instance(self, action_commands, non_action_commands, joins):
        self.dungeon = __import__(self.hub_definition_file_path).dungeon
        super().initialize_instance(action_commands, non_action_commands, joins)
