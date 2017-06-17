from erukar.server.Instance import Instance

class HubInstance(Instance):
    def __init__(self, file_path):
        self.hub_definition_file_path = file_path
        super().__init__()
        self.identifier = file_path

    def initialize_instance(self, connector):
        self.dungeon = __import__(self.hub_definition_file_path).dungeon
        super().initialize_instance(connector)
