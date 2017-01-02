from erukar.data.ConnectorFactory import ConnectorFactory
from erukar.engine.model import *
from erukar.engine.lifeforms.Player import Player
from erukar.server.Interface import Interface
from erukar.server.InstanceInfo import InstanceInfo
import erukar, threading
import numpy as np

class Shard(Manager):
    DefaultInstance = 0

    def __init__(self):
        super().__init__()
        db_pass = ''
        self.connector_factory = ConnectorFactory(db_pass)
        self.connector_factory.establish_connection()
        self.connector_factory.create_metadata()
        self.data = self.connector_factory.create_session()
        self.interface = Interface(self)
        self.instances = []

    def activate(self):
        self.instances = [
            InstanceInfo(erukar.server.HubInstance, {'file_path': 'Test'})
        ]
        for info in self.instances:
            self.launch_dungeon_instance(info)

    def subscribe(self, uid):
        super().subscribe(uid)
        # Check Connector for plaOyer
        player = self.get_playernode_from_uid(uid)
        character = self.get_character_from_playernode(uid)
        self.interface.data.players.append(player)
        print('Check for player\'s desired entry location')
        self.instances[0].player_list.append(player)

    def get_playernode_from_uid(self, uid):
        playernode = self.data.get_player({'uid': uid})
        if playernode is None:
            self.new_player_tutorial()
            playernode = PlayerNode(uid)
            self.data.add_player(playernode)
        return playernode

    def get_character_from_playernode(self, uid):
        character = Player()
        character.uid = uid
        if not self.data.load_player(uid, character):
            print('Need a new character')
            self.data.add_character(uid, character) 
            self.data.update_character(character)
        return character

    def new_player_tutorial(self):
        print('New Player')

    def create_random_dungeon(self, for_player):
        dungeon = InstanceInfo(erukar.server.RandomDungeonInstance, {'level': for_player.level})
        self.launch_dungeon_instance(dungeon)
        return dungeon

    def launch_dungeon_instance(self, info):
        args=(self.connector_factory.create_session(),
              info.action_commands,
              info.non_action_commands,
              info.joins,
        )
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
