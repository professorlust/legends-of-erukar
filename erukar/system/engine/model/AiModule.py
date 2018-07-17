from erukar.ext.math import Pathing


class AiModule:
    def __init__(self, puppet):
        self.puppet = puppet
        self.world = None

    def on_start(self, world):
        self.world = world

    def create_command(self, cmd_type):
        cmd = cmd_type()
        cmd.world = self.world
        cmd.player_info = self.puppet
        cmd.args = {}
        return cmd

    def perform_turn(self):
        return None

    def get_path_to(self, goal):
        if not self.world:
            return []
        start = self.puppet.coordinates
        collection = self.world.all_traversable_coordinates()

        pather = Pathing(collection)
        path_info, cost = pather.search(collection, start, goal)
        path = pather.reverse(path_info, start, goal)
        if path:
            path.pop(0)
        return path
