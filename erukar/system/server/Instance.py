from erukar.system.engine import Manager, Player, PlayerNode, Dead, Enemy
from erukar.system.engine.commands import LocalIndex, Map, Inspect, Inventory
from erukar.system.engine.commands import Stats, Skills, Wait, TargetedCommand, TickExecution
from .TurnManager import TurnManager
from .DifferentialMessageEngine import DifferentialMessageEngine
import erukar
import random
import datetime
import json
import uuid
import logging
logger = logging.getLogger('debug')


class Instance(Manager):
    MaximumTurnTime = 30.0  # In seconds
    MaximumTurnSkipPenalty = 5  # in turns
    TickRate = 0.2  # in seconds

    NotInitialized = -1
    Ready = 0
    Idle = 1
    Running = 2
    Frozen = 3
    Closing = 4

    def __init__(self, location):
        super().__init__()
        self.diff_engine = DifferentialMessageEngine()
        self.properties = None
        self.identifier = str(uuid.uuid4())
        self.location = location
        self.dungeon = None
        self.reset()
        self.players = set()
        self.outbox = {}

    def reset(self):
        self.active_player = None
        self.command_contexts = {}
        self.status = Instance.NotInitialized
        self.responses = {}
        self.characters = []
        self.slain_characters = []
        self.active_interactions = []
        self.outbox = {}

    def initialize_instance(self, session):
        '''Turn on players and generate a dungeon'''
        self.session = session
        self.status = Instance.Ready
        self.turn_manager = TurnManager()
        self.dungeon = self.location.get_dungeon()
        self.dungeon.location = self.location
        self.dungeon.on_start()
        self.subscribe_enemies()
        self.status = Instance.Running
        self.info.on_instance_ready()

    def any_connected_players(self):
        '''Check to see if there are any currently connected players'''
        return any([isinstance(x, PlayerNode) for x in self.players])

    def subscribe_enemies(self):
        for x in self.dungeon.actors:
            if isinstance(x, Enemy):
                self.subscribe_enemy(x)

    def handle_enemy_persistence(self, room, enemy):
        '''Get persisted enemies where available'''
        if not issubclass(type(enemy), Enemy):
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
        node.sector = self.dungeon.overland_location.coordinates()
        random_loc = random.choice(self.dungeon.spawn_coordinates)
        all_coords = self.dungeon.location_transition_coordinates
        spawn_location = all_coords.get(node.previous_location, random_loc)
        self.dungeon.add_actor(node.character, spawn_location)
        if self.active_player is None:
            self.active_player = node
        erukar.data.Character.update(node.character, self.session)
        node.character.uid = node.uid
        self.subscribe_being(node.lifeform())
        self.execute_pre_inspect(node)
        node.lifeform().build_zones(self.dungeon)
        self.turn_manager.subscribe(node)
        self.players.add(node)
        self.give_tile_set(node)
        self.send_update_to(node)

    def subscribe_enemy(self, enemy):
        self.turn_manager.subscribe(enemy)
        self.subscribe_being(enemy)
        self.players.add(enemy)
        enemy.build_zones(self.dungeon)

    def subscribe_being(self, being):
        being.subscribe(self)
        self.command_contexts[being.uid] = None
        self.characters.append(being)
        being.world = self.dungeon
        self.dungeon.add_actor_tiles(being)

        # Run on_equip for all equipped items
        for equip in being.equipment_types:
            equipped = getattr(being, equip)
            if equipped is not None:
                equipped.on_equip(being)

        being.instance = self.identifier

    def unsubscribe(self, node):
        if node not in self.players:
            return
        self.dungeon.remove_actor(node.lifeform())
        self.turn_manager.unsubscribe(node)
        self.players.remove(node)
        self.characters.remove(node.lifeform())
        super().unsubscribe(node)
        self.handle_reduced_player_count()

    def handle_reduced_player_count(self):
        logger.info('Instance -- Reducing player count')

    def try_to_get_persistent_enemy(self, enemy):
        possible_uids = list(self.get_possible_uids(enemy))
        if len(possible_uids) <= 0:
            return
        uid = random.choice(possible_uids)
        return self.connector.load_creature(uid)

    def get_possible_uids(self, enemy):
        for e in self.connector.get_creature_uids():
            if not self.session.find_player(e.uid):
                yield e.uid

    def execute_pre_inspect(self, player):
        player.lifeform().current_action_points += Inspect.ActionPointCost
        ins = player.create_command(Inspect)
        self.try_execute(player, ins)

    def send_update_to_players(self):
        for player in self.players:
            if not isinstance(player, PlayerNode):
                continue
            self.send_update_to(player)

    def handle_all_transitions(self):
        to_trans = list(self.transitioning_players())
        for node in to_trans:
            node.tell('nuke state', json.dumps('{}'))
            self.unsubscribe(node)

    def transitioning_players(self):
        for player in self.players:
            if isinstance(player, PlayerNode)\
              and player.status == PlayerNode.Transitioning:
                yield player

    def try_execute(self, node, cmd, auto_advance=True):
        if not cmd:
            return
        cmd.interactions = self.active_interactions
        if not self.any_connected_players():
            if isinstance(self.active_player, Enemy):
                self.active_player.stop_execution()
            return

        if isinstance(cmd, TargetedCommand):
            return self.try_execute_targeted_command(node, cmd)

        if node.uid == self.active_player.uid:
            self.execute_and_process(cmd, auto_advance)

            # Tell characters
            self.send_update_to_players()
            self.handle_all_transitions()

    def execute_and_process(self, cmd, auto_advance=True):
        '''When conditions allow an executable to be run, execute it
        and run the standard update workflow'''
        result = self.execute_command(cmd)
        if result is None or not result.success:
            return

        for uid in cmd.outbox:
            self.outbox[uid] = self.outbox.get(uid, []) + cmd.outbox[uid]

        if hasattr(result, 'interaction'):
            self.active_interactions.append(result.interaction)

        active_lifeform = self.active_player.lifeform()

        if cmd.RebuildZonesOnSuccess:
            active_lifeform.flag_for_rebuild()

        self.clean_dead_characters()
        self.build_zones_where_necessary()
        self.clean_interactions()

        if not auto_advance:
            return
        if active_lifeform.should_auto_end_turn() or isinstance(cmd, Wait):
            self.get_next_player()

    def build_zones_where_necessary(self):
        for player in self.players:
            if player.lifeform().zones.desynced:
                player.lifeform().build_zones(self.dungeon)

    def try_execute_targeted_command(self, node, cmd):
        result = self.execute_command(cmd)
        if result is None:
            return

        if result.success:
            if hasattr(result, 'interaction'):
                self.active_interactions.append(result.interaction)
            self.clean_interactions()
        self.send_update_to(node)

    def clean_interactions(self):
        for interaction in self.active_interactions:
            for leaving in interaction.leaving:
                self.send_update_to(leaving)
            interaction.clean()
        self.active_interactions = list(self.unended_interactions())

    def unended_interactions(self):
        for x in self.active_interactions:
            if not x.ended:
                yield x

    def clean_dead_characters(self):
        dead_characters = [x for x in self.characters if x.has_condition(Dead)]
        for char in dead_characters:
            node = self.dead_player_node(char)
            self.send_update_to(node)
            self.unsubscribe(node)
            self.slain_characters.append(node)

    def dead_player_node(self, character):
        for x in self.players:
            if x.lifeform() is character:
                return x

    def give_tile_set(self, node):
        node.tell('update tile set', json.dumps(self.dungeon.tile_set))
        node.tile_set_version = self.dungeon.tile_set_version

    def do_non_player_turn(self):
        if not self.should_do_non_player_turn():
            return
        cmd, exec_count = None, 0
        while self.should_continue_non_player_turn(cmd, exec_count):
            cmd = self.active_player.perform_turn()
            self.try_execute(self.active_player, cmd, auto_advance=False)
            exec_count += 1
        self.get_next_player()

    def should_do_non_player_turn(self):
        return issubclass(type(self.active_player), Enemy)\
            and not self.active_player.is_incapacitated()

    def should_continue_non_player_turn(self, cmd, exec_count):
        return not isinstance(cmd, Wait)\
                and not self.active_player.should_pass()\
                and exec_count < 4

    def active_player_is_player(self):
        return self.active_player is not None\
            and not isinstance(self.active_player, str)

    def get_next_player(self):
        if len(list(self.real_players())) <= 0:
            return
        if self.active_player_is_player():
            cmd = TickExecution()
            cmd.world = self.dungeon
            self.active_player.end_turn(cmd)
            result = cmd.execute()
            self.append_result_responses(result)

        self.active_player = self.turn_manager.next()
        if self.active_player_is_player():
            cmd = TickExecution()
            cmd.world = self.dungeon
            self.active_player.begin_turn(cmd)
            result = cmd.execute()
            uid = self.active_player.uid
            self.outbox[uid] = self.outbox.get('uid', []) + [{
                'change': 'your turn',
                'data': []
            }]
            self.append_result_responses(result)
            self.send_update_to(self.active_player)

        if isinstance(self.active_player, str):
            self.tick()
        else:
            self.active_player.lifeform().flag_for_rebuild()

        # Update players
        if isinstance(self.active_player, Enemy):
            self.do_non_player_turn()

    def tick(self):
        cmd = TickExecution()
        cmd.world = self.dungeon
        self.dungeon.tick(cmd)
        for player in self.players:
            player.lifeform().tick(cmd)
        result = cmd.execute()
        self.append_result_responses(result)
        self.send_update_to_players()
        self.get_next_player()

    def real_players(self):
        for player in self.players:
            if isinstance(player, PlayerNode):
                yield player

    def execute_command(self, cmd):
        cmd.server_properties = self.properties
        cmd.context = self.command_contexts[cmd.player_info.uid]
        if cmd.context and not hasattr(cmd.context, 'server_properties'):
            cmd.context.server_properties = self.properties
        cmd.world = self.dungeon
        result = cmd.execute()

        # Check results
        if result is not None:
            self.subscribe_new_characters(cmd.added_characters)
            # Print Result, replace with outbox later
            if hasattr(result, 'results'):
                self.append_result_responses(result)

            # Save Dirtied Characters in DB
            if hasattr(result, 'dirtied_characters'):
                for dirty in result.dirtied_characters:
                    if isinstance(dirty, Player):
                        erukar.data.Character.update(dirty, self.session)

            # Set context for player
            self.command_contexts[cmd.player_info.uid] = result

        return result

    def subscribe_new_characters(self, added):
        for character in added:
            self.subscribe_enemy(character)

    def append_result_responses(self, result):
        for uid in result.results:
            response = '\n'.join(result.result_for(uid)) + '\n'
            self.append_response(uid, response)

    def append_response(self, uid, response):
        if uid not in self.responses:
            self.responses[uid] = [response]
            return
        self.responses[uid] = self.responses[uid] + [response]

    def get_messages_for(self, node):
        if not node:
            yield 'joining', Instance.waiting_to_join()
        self.send_tile_set_if_necessary(node)

        log = list(self.convert_responses_to_log(node))
        if node in self.slain_characters:
            yield 'you died', json.dumps({'log': log})

    def waiting_to_join():
        return json.dumps({
            'log': {
                'text': 'Waiting to join',
                'when': str(datetime.datetime.now())
            }
        })

    def convert_responses_to_log(self, node):
        if node.uid in self.responses and len(self.responses[node.uid]) > 0:
            responses = self.responses.pop(node.uid, [])
            for line in responses:
                yield {
                    'text': line,
                    'when': str(datetime.datetime.now())
                }

    def send_tile_set_if_necessary(self, node):
        if self.dungeon.tile_set_version > node.tile_set_version:
            self.give_tile_set(node)

    def get_interaction_results(self, node):
        interaction_state = {}
        for interaction in self.active_interactions:
            if node not in interaction.involved:
                continue
            result = interaction.get_result_for(node)
            interaction_state[str(interaction.uuid)] = result
        return interaction_state

    def send_update_to(self, node):
        if not isinstance(node, PlayerNode):
            return

        outbox = self.outbox.pop(node.uid, [])
        log = list(self.convert_responses_to_log(node))
        for msg in outbox:
            node.tell(msg['change'], json.dumps(msg['data']))
        for _type, msg in self.diff_engine.messages_for(self, node, log):
            node.tell(_type, json.dumps(msg))
