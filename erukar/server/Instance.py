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
from erukar.engine.commands.executable.Skills import Skills
from erukar.engine.commands.executable.Wait import Wait
from erukar.engine.conditions.Dead import Dead
import erukar, threading, random, datetime, json, uuid

import logging
logger = logging.getLogger('debug')

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
        self.characters = []
        self.slain_characters = []

    def initialize_instance(self, session):
        '''Turn on players and generate a dungeon'''
        self.session = session
        self.status = Instance.Ready
        self.turn_manager = TurnManager()
        if self.dungeon:
            self.on_start()

    def on_start(self):
        self.dungeon.on_start()
        self.subscribe_enemies()
        for room in self.dungeon.rooms:
            room.on_start()
        self.status = Instance.Running
        self.info.on_instance_ready()

    def any_connected_players(self):
        '''Check to see if there are any currently connected players'''
        return any([isinstance(x, PlayerNode) for x in self.players])

    def subscribe_enemies(self):
        for x in self.dungeon.actors:
            if isinstance(x, erukar.engine.lifeforms.Enemy):
                self.subscribe_enemy(x)

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

    def subscribe(self, node):
        '''Subscribe a player'''
        if not hasattr(node, 'character') or node.character is None:
            raise Exception("No character")

        node.world = self.dungeon
        self.dungeon.add_actor(node.character, random.choice(self.dungeon.spawn_coordinates))
        if self.active_player is None: self.active_player = node

        erukar.data.models.Character.update(node.character, self.session)
        node.character.uid = node.uid
        self.subscribe_being(node.lifeform())
        self.execute_pre_inspect(node)
        node.lifeform().build_zones(self.dungeon)
        self.turn_manager.subscribe(node)
        super().subscribe(node)
        self.send_update_to(node)
        self.give_tile_set(node)

    def subscribe_enemy(self, enemy):
        self.turn_manager.subscribe(enemy)
        self.subscribe_being(enemy)
        super().subscribe(enemy)
        enemy.build_zones(self.dungeon)

    def subscribe_being(self, being):
        being.subscribe(self)
        self.command_contexts[being.uid] = None
        self.characters.append(being)
        being.world = self.dungeon

        # Run on_equip for all equipped items
        for equip in being.equipment_types:
            equipped = getattr(being, equip)
            if equipped is not None:
                equipped.on_equip(being)

        being.instance = self.identifier

    def unsubscribe(self, node):
        if node not in self.players:
            logger.info('Instance -- No player could be found matching {}'.format(node))
            return
        logger.info('Instance -- Removing {}'.format(node))
        self.dungeon.remove_actor(node.lifeform())
        self.turn_manager.unsubscribe(node)
        self.players.remove(node)
        self.characters.remove(node.lifeform())
        super().unsubscribe(node)
        self.handle_reduced_player_count()

    def handle_reduced_player_count(self):
        logger.info('Instance -- Reducing player count')

    def try_to_get_persistent_enemy(self, enemy):
        possible_uids = [e.uid for e in self.connector.get_creature_uids() if not self.session.find_player(e.uid)]
        if len(possible_uids) <= 0: 
            return
        uid = random.choice(possible_uids)
        return self.connector.load_creature(uid)

    def execute_pre_inspect(self, player):
        player.lifeform().current_action_points += Inspect.ActionPointCost
        ins = player.create_command(Inspect)
        self.try_execute(player, ins)

    def try_execute(self, node, cmd):
        if not self.any_connected_players():
            if isinstance(self.active_player, erukar.engine.lifeforms.Enemy):
                self.active_player.stop_execution()
            return

        if node.uid == self.active_player.uid:
            result = self.execute_command(cmd)
            if result is None or (result is not None and not result.success):
                return

            if cmd.RebuildZonesOnSuccess:
                self.active_player.lifeform().flag_for_rebuild()

            self.clean_dead_characters()

            if self.active_player.lifeform().action_points() == 0 or isinstance(cmd, Wait):
                self.get_next_player()

            # Tell characters
            to_tell = [x for x in self.players if isinstance(x, PlayerNode)]
            for node in to_tell:
                self.send_update_to(node)


    def clean_dead_characters(self):
        dead_characters = [x for x in self.characters if x.has_condition(Dead)]
        for char in dead_characters:
            node = next((x for x in self.players if x.lifeform() is char), None)
            self.send_update_to(node) 
            
            self.unsubscribe(node)
            self.slain_characters.append(node)

    def send_update_to(self, node):
        if not isinstance(node, PlayerNode): return
        msgs = self.get_messages_for(node)
        node.tell('update state', msgs)

    def give_tile_set(self, node):
        node.tell('update tile set', json.dumps(self.dungeon.tile_set))

    def do_non_player_turn(self):
        if issubclass(type(self.active_player), erukar.engine.lifeforms.Enemy):
            if not self.active_player.is_incapacitated():
                self.active_player.perform_turn(self)

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

        if isinstance(self.active_player, str):
            self.tick()

        if isinstance(self.active_player, erukar.engine.lifeforms.Enemy):
            self.do_non_player_turn()

    def tick(self):
        self.dungeon.tick()
        for player in self.players:
            player.lifeform().tick()
        self.get_next_player()

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

        return result

    def append_result_responses(self, result):
        for uid in result.results:
            self.append_response(uid,'\n'.join(result.result_for(uid)) + '\n')

    def append_response(self, uid, response):
        if uid not in self.responses:
            self.responses[uid] = [response]
            return
        self.responses[uid] = self.responses[uid] + [response]

    def get_messages_for(self, node):
        if not node:
            return json.dumps({'log': {'text': 'Waiting to join', 'when': str(datetime.datetime.now())}})

        log = []
        if node.uid in self.responses and len(self.responses[node.uid]) > 0:
            responses =  self.responses.pop(node.uid, [])
            for line in responses:
                log.append({'text':line, 'when': str(datetime.datetime.now())})

        if node in self.slain_characters:
            return json.dumps({'log': log})

        character = node.lifeform()
        d = self.dungeon

        inv_cmd = node.create_command(Inventory)
        result = inv_cmd.execute()
        inv_res = result.result_for(node.uid)[0]

        stat_cmd = node.create_command(Stats)
        stat_res = stat_cmd.execute().result_for(node.uid)

        skill_cmd = node.create_command(Skills)
        skill_res = skill_cmd.execute().result_for(node.uid)

        map_cmd = node.create_command(Map)
        map_res = map_cmd.execute().result_for(node.uid)

        li_cmd = node.create_command(LocalIndex)
        li_res = li_cmd.execute().result_for(node.uid)

        return json.dumps({
            'turnOrder': self.turn_manager.frontend_readable_turn_order()[:4],
            'statPoints': character.stat_points,
            'skillPoints': character.skill_points,
            'skills': skill_res[0],
            'actionPoints': { 'current': character.current_action_points, 'reserved': character.reserved_action_points },
            'inventory': inv_res['inventory'],
            'equipment': inv_res['equipment'],
            'vitals': stat_res[0],
            'map': map_res[0],
            'localList': li_res[0],
            'log': log
        })
