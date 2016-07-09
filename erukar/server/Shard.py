from erukar.engine.model import * 
from erukar.server.Instance import Instance
from erukar.server.Interface import Interface
import threading
import numpy as np

class Shard(Manager):
    def __init__(self):
        super().__init__()
        self.interface = Interface()
        self.dungeons = []

    def activate(self):
        self.dungeons = [Instance()]
        for dungeon in self.dungeons:
            gen_params = GenerationProfile(*(np.random.uniform(-1, 1) for x in range(4)))
            self.launch_dungeon_instance(dungeon, gen_params)

    def subscribe(self, player):
        super().subscribe(player)
        self.interface.data.players.append(player)

    def launch_dungeon_instance(self, dungeon, gen_params):
        args=(self.interface.requests, gen_params,)
        dungeon_thread = threading.Thread(target=dungeon.instance_running,args=args)
        dungeon_thread.daemon = True
        dungeon_thread.start()
