from erukar.engine.model.Manager import Manager
from erukar.data.Connector import Connector
from erukar.server.TurnManager import TurnManager
from erukar.engine.lifeforms.Player import Player
from erukar.engine.model.PlayerNode import PlayerNode
from erukar.engine.commands.executable.LocalIndex import LocalIndex
from erukar.engine.commands.executable.Map import Map
from erukar.engine.commands.executable.Inspect import Inspect
from erukar.engine.commands.executable.Inventory import Inventory
from erukar.engine.commands.executable.Stats import Stats
from erukar.engine.commands.executable.Wait import Wait
import erukar, threading, random, datetime, json, uuid

import logging
InstanceLogger = logging.getLogger('instance')
InstanceLogger.setLevel(logging.INFO)
fh = logging.FileHandler('instance.log')
InstanceLogger.addHandler(fh)

class Instance(Manager):
    MaximumTurnTime = 30.0 # In seconds
    MaximumTurnSkipPenalty = 5 # in turns
    TickRate = 0.2 # in seconds

    NotInitialized = -1
    Ready = 0
    Idle = 1
    Running = 2
    Frozen = 3
    Closing = 4

    def __init__(self):
        super().__init__()
        self.properties = None
        self.identifier = str(uuid.uuid4())
        self.dungeon = None
        self.reset()

    def reset(self):
        self.active_player = None
        self.command_contexts = {}
        self.status = Instance.NotInitialized
        self.responses = {}

    def initialize_instance(self, session):
        '''Turn on players and generate a dungeon'''
        self.session = session
        self.status = Instance.Ready
        self.turn_manager = TurnManager()
        if self.dungeon:
            self.on_start()

    def on_start(self):
        self.subscribe_enemies()
        for room in self.dungeon.rooms:
            room.on_start()
        self.status = Instance.Running
        self.info.on_instance_ready()

    def any_connected_players(self):
        '''Check to see if there are any currently connected players'''
        return any([isinstance(x, PlayerNode) for x in self.players])

    def subscribe_enemies(self):
        for room in self.dungeon.rooms:
            for item in room.contents:
                self.handle_enemy_persistence(room, item)
            room.contents = [c for c in room.contents if not (isinstance(type(c), erukar.engine.lifeforms.Enemy) and c.requesting_persisted)]

    def handle_enemy_persistence(self, room, enemy):
        '''Get persisted enemies where available'''
        if not issubclass(type(enemy), erukar.engine.lifeforms.Enemy):
            return

        if enemy.requesting_persisted:
            persisted_enemy = self.try_to_get_persistent_enemy(enemy)
            if persisted_enemy:
                persisted_enemy.link_to_room(room)
                persisted_enemy.is_transient = False
                self.subscribe_enemy(persisted_enemy)
            return

        self.subscribe_enemy(enemy)

    def subscribe_enemy(self, enemy):
        enemy.subscribe(self)
        self.command_contexts[enemy.uid] = None
        self.turn_manager.subscribe(enemy)
        self.players.append(enemy)

    def unsubscribe(self, eid):
        player = next((x for x in self.players if x.uid == eid), None)
        if not player: return
        self.dungeon.remove_actor(player.lifeform())
        self.turn_manager.unsubscribe(player)
        self.players.remove(player)
        super().unsubscribe(player)

    def try_to_get_persistent_enemy(self, enemy):
        possible_uids = [e.uid for e in self.connector.get_creature_uids() if not self.session.find_player(e.uid)]
        if len(possible_uids) <= 0: 
            return
        uid = random.choice(possible_uids)
        return self.connector.load_creature(uid)

    def subscribe(self, node):
        InstanceLogger.info(self.identifier)
        if not hasattr(node, 'character') or node.character is None:
            raise Exception("No character")

        node.world = self.dungeon
        node.character.world = self.dungeon
        super().subscribe(node)
        self.dungeon.add_actor(node.character, random.choice(self.dungeon.spawn_coordinates))
        if self.active_player is None: self.active_player = node

        # Run on_equip for all equipped items
        for equip in node.character.equipment_types:
            equipped = getattr(node.character, equip)
            if equipped is not None:
                equipped.on_equip(node.character)

        node.character.instance = self.identifier
        erukar.data.models.Character.update(node.character, self.session)
        self.turn_manager.subscribe(node)
        self.command_contexts[node.uid] = None
        self.execute_pre_inspect(node)

    def execute_pre_inspect(self, player):
        player.lifeform().current_action_points += Inspect.ActionPointCost
        ins = player.create_command(Inspect)
        self.try_execute(player, ins)

    def try_execute(self, node, cmd):
        if node.uid == self.active_player.uid:
            result = self.execute_command(cmd)
            if result is None or (result is not None and not result.success):
                return

            if self.active_player.lifeform().action_points() == 0 or isinstance(cmd, Wait):
                self.get_next_player()

        # Go ahead and execute ai turns
        while self.turn_manager.has_players() and not isinstance(self.active_player, erukar.engine.model.PlayerNode):
            self.do_non_player_turn()

    def do_non_player_turn(self):
        if isinstance(self.active_player, str):
            self.tick()
    
        if issubclass(type(self.active_player), erukar.engine.lifeforms.Enemy):
            if not self.active_player.is_incapacitated():
                self.execute_ai_turn()

        self.get_next_player()

    def execute_ai_turn(self):
        cmd = self.active_player.perform_turn()
        if cmd is not None:
            result = self.execute_command(cmd)

    def get_next_player(self):
        if self.active_player is not None and not isinstance(self.active_player, str):
            res = self.active_player.end_turn()
            if len(res) > 0:
                self.append_response(self.active_player.uid, res)

        self.active_player = self.turn_manager.next()
        if self.active_player is not None and not isinstance(self.active_player, str):
            res = self.active_player.begin_turn()
            if len(res) > 0:
                self.append_response(self.active_player.uid, res)

    def tick(self):
        self.dungeon.tick()
        for player in self.players:
            player.lifeform().tick()

    def execute_command(self, cmd):
        cmd.server_properties = self.properties
        cmd.context = self.command_contexts[cmd.player_info.uid]
        if cmd.context and not hasattr(cmd.context, 'server_properties'):
            cmd.context.server_properties = self.properties
        cmd.world = self.dungeon
        result = cmd.execute()

        # Check results
        if result is not None:
            # Print Result, replace with outbox later
            if hasattr(result, 'results'):
                self.append_result_responses(result)

            # Save Dirtied Characters in DB 
            if hasattr(result, 'dirtied_characters'):
                for dirty in result.dirtied_characters:
                    if isinstance(dirty, erukar.engine.lifeforms.Player):
                        erukar.data.models.Character.update(dirty, self.session)

            # Set context for player
            self.command_contexts[cmd.player_info.uid] = result

        self.check_for_transitions(result)
        return result

    def check_for_transitions(self, result):
        for player in self.players:
            if hasattr(player.lifeform(), 'transition_properties') and player.lifeform().transition_properties is not None:
                self.unsubscribe(player)

    def append_result_responses(self, result):
        for uid in result.results:
            self.append_response(uid,'\n'.join(result.result_for(uid)) + '\n')

    def append_response(self, uid, response):
        if uid not in self.responses:
            self.responses[uid] = [response]
            return
        self.responses[uid] = self.responses[uid] + [response]

    def get_messages_for(self, uid):
        player_node = self.get_player_from_uid(uid)
        if not player_node:
            InstanceLogger.info([x.uid for x in self.players])
            return json.dumps({'log': {'text': 'Waiting to join', 'when': str(datetime.datetime.now())}})

        character = player_node.lifeform()
        d = self.dungeon

        inv_cmd = player_node.create_command(Inventory)
        result = inv_cmd.execute()
        inv_res = result.result_for(player_node.uid)[0]

        stat_cmd = player_node.create_command(Stats)
        stat_res = stat_cmd.execute().result_for(player_node.uid)

        map_cmd = player_node.create_command(Map)
        map_res = map_cmd.execute().result_for(player_node.uid)

        li_cmd = player_node.create_command(LocalIndex)
        li_res = li_cmd.execute().result_for(player_node.uid)

        log = []
        if uid in self.responses and len(self.responses[uid]) > 0:
            responses =  self.responses.pop(uid, [])
            for line in responses:
                log.append({'text':line, 'when': str(datetime.datetime.now())})

        return json.dumps({
            'turnOrder': self.turn_manager.frontend_readable_turn_order()[:4],
            'statPoints': character.stat_points,
            'skillPoints': character.skill_points,
            'actionPoints': { 'current': character.current_action_points, 'reserved': character.reserved_action_points },
            'inventory': inv_res['inventory'],
            'equipment': inv_res['equipment'],
            'vitals': stat_res[0],
            'map': map_res[0],
            'localList': li_res[0],
            'log': log
        })
