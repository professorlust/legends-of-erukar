from erukar.server.Instance import Instance
from erukar.server.Interface import Interface

class InstanceInfo:
    '''
    Small object which exists on the main thread that keeps track
    of information that the Shard should know about a Dungeon 
    Instance, e.g. PlayerList, command_queue, command results list 
    '''
    def __init__(self):
        self.instance = Instance()
        self.player_list = []
        self.command_queue = []
        self.command_results_list = []
