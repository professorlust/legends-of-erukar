from erukar.server.Instance import Instance

class HubInstance(Instance):
    def __init__(self, file_path):
        self.hub_definition_file_path = file_path
        super().__init__()

    def activate(self, action_commands, non_action_commands, joins, generation_parameters):
        self.dungeon = __import__(self.hub_definition_file_path).dungeon
        super().activate(action_commands, non_action_commands, joins, generation_parameters)
