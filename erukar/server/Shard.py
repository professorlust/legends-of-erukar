from erukar.engine.model import * 
from erukar.server.Interface import Interface
from erukar.server.InstanceInfo import InstanceInfo
import threading
import numpy as np

class Shard(Manager):
    def __init__(self):
        super().__init__()
        self.interface = Interface(self)
        self.instances = []

    def activate(self):
        self.instances = [InstanceInfo()]
        for info in self.instances:
            gen_params = GenerationProfile(*(np.random.uniform(-1, 1) for x in range(4)))
            self.launch_dungeon_instance(info, gen_params)

    def subscribe(self, player):
        super().subscribe(player)
        #Hardcode this for now until I figure out join logic
        self.instances[0].player_list.append(player)
        self.interface.data.players.append(player)

    def launch_dungeon_instance(self, info, gen_params):
        args=(info.action_commands, info.non_action_commands,  gen_params,)
        dungeon_thread = threading.Thread(target=info.instance.instance_running,args=args)
        dungeon_thread.daemon = True
        dungeon_thread.start()

    def player_current_instance(self, uid):
        for info in self.instances:
            if uid in list(self.uids_in_instance(info)):
                return info

    def uids_in_instance(self, info):
        for player in info.player_list:
            yield player.uid
