from erukar.engine.commands.executable.Inventory import Inventory
from erukar.engine.commands.executable.Stats import Stats
from erukar.data.ConnectorFactory import ConnectorFactory
from erukar.engine.model import *
from erukar.engine.lifeforms.Player import Player
from erukar.server.Interface import Interface
from erukar.server.InstanceInfo import InstanceInfo
from erukar.server.ServerProperties import ServerProperties
from erukar.server.Connection import Connection
import erukar, threading, json, asyncio
import numpy as np

class Shard(Manager):
    SplashPath = 'Splash'
    CharacterCreationPath = 'CharacterSelect'
    TutorialPath = 'Tutorial'

    def __init__(self, emit_fn):
        super().__init__()
        db_pass = ''
        self.connector_factory = ConnectorFactory(db_pass)
        self.connector_factory.establish_connection()
        self.connector_factory.create_metadata()
        self.properties = ServerProperties()
        self.data = self.connector_factory.create_session()
        self.interface = Interface(self)
        self.instances = []
        self.clients = set()
        self.outbox = {}
        self.emit = emit_fn

    def activate(self):
        '''
        Create all Hub Instances and spin up  
        '''
        __import__('Templates').configure(self)
        __import__('ServerProperties').configure(self)
        __import__('WorldConfiguration').configure(self)
        __import__('Arcana').configure(self)

        self.instances = [
            InstanceInfo(erukar.server.HubInstance, self.properties.copy(), {'file_path': option})
            for option in self.StartingOptions
        ]
        for info in self.instances:
            self.launch_dungeon_instance(info)

    def get_client(self, request):
        addr = request.environ['REMOTE_ADDR']
        return next((c for c in self.clients if c.addr == addr), None)

    def update_connection(self, request):
        '''Update a connection with sid or http_port if necessary'''
        con = self.get_client(request)
        if not con:
            con = Connection(request.environ['REMOTE_ADDR'], self.emit)
            self.clients.add(con)

        # If we have a sid and an http_port, we're finalized
        if con.is_finalized(): return con

        # Only add the sid if this is a socket request and we don't have a sid already
        if hasattr(request, 'sid'):
            if not con.sid:
                con.sid = request.sid
            return con

        if not con.http_port:
            con.http_port = request.environ['REMOTE_PORT']
        return con

    def disconnect(self, request):
        con = self.get_client(request)
        if con is None: return
        self.clients.remove(con)

    def login(self, uid):
        return self.data.get_player({'uid': uid})

    def unsubscribe(self, eid):
        player = self.get_playernode_from_uid(eid)
        cur_instance = self.player_current_instance(eid)
        if cur_instance:
            return cur_instance.instance.unsubscribe(eid)
        super().unsubscribe(eid)

    def subscribe(self, player):
        '''Called when a player (with uid) is connecting'''
        if player not in self.connected_players:
            self.connected_players.add(player)
        self.establish_playernode(player)
        
    def establish_playernode(self, player):
        player.status = PlayerNode.SelectingCharacter
        # fix this
        _, characters = self.data.get_player({'uid':player.uid})
        message = json.dumps({
            'type': 'characterList',
            'characters': [Shard.format_character_for_list(c) for c in characters]
        })
        self.add_to_outbox(player.uid, message)

    def format_character_for_list(c):
        return {
            'id': c.id,
            'name': c.name,
            'deceased': c.deceased,
            'level': c.level,
            'wealth': c.wealth,
            'strength': c.strength,
            'dexterity': c.dexterity,
            'vitality': c.vitality,
            'acuity': c.acuity,
            'sense': c.sense,
            'resolve': c.resolve
        }

    def add_to_outbox(self, uid, message):
        self.emit('outbound', message)

    def start_playing(self, playernode, character):
        '''Callback from character creation or subscription'''
        if not character: return
        playernode.character = character
        info = self.get_instance_for(character, character.instance)
        self.move_player_to_instance(playernode, info)
        playernode.status = PlayerNode.Playing
        self.add_to_outbox(playernode.uid, json.dumps({'type': 'playing'}))

    def move_player_to_instance(self, node, info):
        if info.instance.dungeon:
            self.interface.append_result(node.uid, '\n'.join([
                '-'*16,
                'Loading {}'.format(info.instance.dungeon.name),
                '{}, {}'.format(info.instance.dungeon.region, info.instance.dungeon.sovereignty),
                '\n{}'.format(info.instance.dungeon.description),
                '-'*16,
                '\n'
            ]))
        else:
            self.interface.append_result(node.uid, '\n'.join([
                '-'*16,
                'Randomizing dungeon',
                '-'*16
            ]))
        info.player_join(node)

    def get_playernode_from_uid(self, uid):
        '''
        Attempt to get a PlayerNode by UID from the database. If it exists,
        return it. If not, run the script @TutorialPath and add the new uid
        to the database.
        '''
        playernode, __ = self.data.get_player({'uid': uid})
        if playernode is None:
            # Run a tutorial for the new guy
            playernode = PlayerNode(uid)
            self.data.add_player(playernode)
        return playernode

    def create_random_dungeon(self, for_player, generation_properties=None, previous_identifier=''):
        '''Create a random dungeon instance based on a player's level'''
        dungeon_info = InstanceInfo(erukar.server.RandomDungeonInstance, self.properties.copy(), {
            'level': for_player.level,
            'generation_properties': generation_properties,
            'previous_identifier': previous_identifier})
        self.launch_dungeon_instance(dungeon_info)
        self.instances.append(dungeon_info)
        return dungeon_info

    def launch_dungeon_instance(self, info):
        '''Launch an instance using an InstanceInfo object.'''
        info.launch(self.connector_factory.create_session())

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

    def get_instance_for(self, character, instance_identifier):
        '''Tries to find an active instance for whatever the character has marked'''
        instance = next((x for x in self.instances if x.identifier == instance_identifier), None)
        if instance is None:
            return self.create_random_dungeon(character)
        return instance

    def transfer_instances(self, uid, properties):
        playernode = self.data.get_player({'uid': uid})
        character = self.get_character_from_playernode(playernode)
        if properties.is_random:
            info = self.create_random_dungeon(character, properties.generation_properties, properties.previous_identifier)
        else:
            info = self.get_instance_for(character, properties.identifier)
        self.move_player_to_instance(uid, info)

    def get_state_for(self, uid):
        cur_instance = self.player_current_instance(uid)
        if cur_instance is not None:
            return cur_instance.instance.get_messages_for(uid)

    def consume_command(self, request, cmd):
        cmd_object = json.loads(cmd)
        client = self.get_client(request)
        if client.playernode is not None and client.playernode.status == PlayerNode.Playing:
            self.interface.receive(client.playernode, cmd_object)

    def active_players(self):
        return len([c for c in self.clients if c.playernode is not None])
