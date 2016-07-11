from erukar.engine.model import * 
from erukar.server.Interface import Interface
from erukar.server.InstanceInfo import InstanceInfo
import threading
import numpy as np

class Shard(Manager):
    def __init__(self):
        super().__init__()
        self.interface = Interface()
        self.dungeons = []

    def activate(self):
        self.instances = [InstanceInfo()]
        for info in self.instances:
            gen_params = GenerationProfile(*(np.random.uniform(-1, 1) for x in range(4)))
            self.launch_dungeon_instance(info.instance, gen_params)

    def subscribe(self, player):
        super().subscribe(player)
        self.interface.data.players.append(player)

    def launch_dungeon_instance(self, instance, gen_params):
        args=(self.interface.requests, gen_params,)
        dungeon_thread = threading.Thread(target=instance.instance_running,args=args)
        dungeon_thread.daemon = True
        dungeon_thread.start()
