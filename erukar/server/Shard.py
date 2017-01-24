from erukar.data.ConnectorFactory import ConnectorFactory
from erukar.engine.model import *
from erukar.engine.lifeforms.Player import Player
from erukar.server.Interface import Interface
from erukar.server.InstanceInfo import InstanceInfo
from erukar.server.ServerProperties import ServerProperties
import erukar, threading
import numpy as np

class Shard(Manager):
    SplashPath = 'Splash'
    CharacterCreationPath = 'CharacterSelect'
    TutorialPath = 'Tutorial'

    def __init__(self):
        super().__init__()
        db_pass = ''
        self.connector_factory = ConnectorFactory(db_pass)
        self.connector_factory.establish_connection()
        self.connector_factory.create_metadata()
        self.properties = ServerProperties()
        self.data = self.connector_factory.create_session()
        self.interface = Interface(self)
        self.instances = []
        self.connected_players = set()

    def activate(self):
        '''
        Create all Hub Instances and spin up  
        '''
        __import__('ServerProperties').configure(self)
        __import__('WorldConfiguration').configure(self)
        __import__('Arcana').configure(self)

        self.instances = [
            InstanceInfo(erukar.server.HubInstance, self.properties.copy(), {'file_path': option})
            for option in self.StartingOptions
        ]
        for info in self.instances:
            self.launch_dungeon_instance(info)

    def subscribe(self, uid):
        '''Called when a player (with uid) is connecting'''
        self.run_script(self.SplashPath, uid)
        super().subscribe(uid)
        # Check Connector for plaOyer
        player = self.get_playernode_from_uid(uid)
        self.interface.data.players.append(player)
        self.connected_players.add(player)
        character = self.get_character_from_playernode(player)
        if character:
            self.start_playing(uid, character)

    def start_playing(self, uid, character):
        '''Callback from character creation or subscription'''
        self.get_active_playernode(uid).status = PlayerNode.Playing
        info = self.get_instance_for(character)
        self.move_player_to_instance(uid, info)

    def move_player_to_instance(self, uid, info):
        if info.instance.dungeon:
            self.interface.append_result(uid, '\n'.join([
                '-'*16,
                'Loading {}'.format(info.instance.dungeon.name),
                '{}, {}'.format(info.instance.dungeon.region, info.instance.dungeon.sovereignty),
                '\n{}'.format(info.instance.dungeon.description),
                '-'*16,
                '\n'
            ]))
        else:
            self.interface.append_result(uid, '\n'.join([
                '-'*16,
                'Randomizing dungeon',
                '-'*16
            ]))
        info.player_join(uid)

    def get_playernode_from_uid(self, uid):
        '''
        Attempt to get a PlayerNode by UID from the database. If it exists,
        return it. If not, run the script @TutorialPath and add the new uid
        to the database.
        '''
        playernode = self.data.get_player({'uid': uid})
        if playernode is None:
            # Run a tutorial for the new guy
            self.run_script(self.TutorialPath, uid)
            playernode = PlayerNode(uid)
            self.data.add_player(playernode)
        return playernode

    def get_character_from_playernode(self, playernode):
        '''
        Attempt to get a not deceased character from the database. If it exists,
        return it. Otherwise, run the player through the script @CharacterCreationPath
        '''
        uid = playernode.uid
        playernode.character = Player()
        playernode.character.uid = uid
        if not self.data.load_player(uid, playernode.character):
            playernode.script_completion_callback = self.character_creation_callback
            self.run_script(self.CharacterCreationPath, uid, playernode)
            return
        return playernode.character

    def character_creation_callback(self, playernode):
        '''
        Callback from the CharacterCreation script. Adds the character to the database
        and then starts playing.
        '''
        self.data.add_character(playernode.uid, playernode.character) 
        self.data.update_character(playernode.character)
        self.start_playing(playernode.uid, playernode.character)

    def run_script(self, script, uid, playernode=None, character=None):
        '''
        Execute a script within `./config/scripts`. When finished, each script should
        call the callback function, though some may get away with not doing so
        (e.g. Splash)
        '''
        if not playernode:
            playernode = self.get_active_playernode(uid)
        payload = ScriptPayload(self, uid, playernode, character, '')
        if playernode:
            playernode.run_script(script)
        __import__(script).run_script(payload)

    def continue_script(self, playernode, user_input):
        '''
        Execute a script within `./config/scripts`. When finished, each script should
        call the callback function, though some may get away with not doing so
        (e.g. Splash)
        '''
        payload = ScriptPayload(self, playernode.uid, playernode, playernode.character, user_input)
        getattr(__import__(playernode.active_script), playernode.script_entry_point)(payload)

    def create_random_dungeon(self, for_player, generation_properties=None):
        '''
        Create a random dungeon instance based on a player's level
        '''
        dungeon_info = InstanceInfo(erukar.server.RandomDungeonInstance, self.properties.copy(), {'level': for_player.level, 'generation_properties': generation_properties})
        self.launch_dungeon_instance(dungeon_info)
        self.instances.append(dungeon_info)
        return dungeon_info

    def launch_dungeon_instance(self, info):
        '''
        Launch an instance using an InstanceInfo object.
        '''
        args=(self.connector_factory.create_session(),
              info.action_commands,
              info.non_action_commands,
              info.sys_messages,
              info.responses,
        )
        dungeon_thread = threading.Thread(target=info.instance.instance_running,args=args)
        dungeon_thread.daemon = True
        dungeon_thread.start()

    def player_current_instance(self, uid):
        for info in self.instances:
            if uid in list(self.uids_in_instance(info)):
                return info

    def uids_in_instance(self, info):
        for uid in info.player_list:
            yield uid

    def is_playing(self, uid):
        return self.get_active_playernode(uid).status == PlayerNode.Playing

    def get_active_playernode(self, uid):
        return next((x for x in self.connected_players if x.uid == uid), None)

    def get_instance_for(self, player):
        '''Tries to find an active instance for whatever the character has marked'''
        instance = next((x for x in self.instances if x.identifier == player.instance), None)
        if instance is None:
            return self.create_random_dungeon(player)
        return instance

    def transfer_instances(self, uid, properties):
        playernode = self.data.get_player({'uid': uid})
        character = self.get_character_from_playernode(playernode)
        if properties.is_random:
            info = self.create_random_dungeon(character, properties.generation_properties)
        else:
            info = self.get_instance_for(character)
        self.move_player_to_instance(uid, info)
