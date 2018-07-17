from erukar.system.engine import SearchScope, Lifeform
from .CommandResult import CommandResult
import uuid


class Command:
    SearchTargetMustBeIndexed = False
    LimitToLocal = False
    NeedsArgs = True
    RebuildZonesOnSuccess = False

    def __init__(self):
        '''These parameters are assigned after instantiation'''
        self.search_scope = SearchScope.World
        self.player_info = None
        self.world = None
        self.args = {}
        self.dirtied_characters = []
        self.added_characters = []
        self.results = {}
        self.outbox = {}

    def process_args(self):
        if not self.args:
            if not self.NeedsArgs:
                self.args = {'player_lifeform': self.player_info.lifeform() }
                return
            raise Exception('Cannot process args -- Command\'s args are undefined')

        self.args['player_lifeform'] = self.player_info.lifeform()

        # Go through all uuids in args and replace with object refs
        if not self.world: raise Exception('Cannot process args -- Command\'s world is undefined')
        for argument in self.args:
            try: arg_uuid = self.get_uuid_for_argument(argument)
            except: continue

            # Try World
            if self.search_scope == SearchScope.World or self.search_scope == SearchScope.Both:
                obj = self.world.get_object_by_uuid(arg_uuid)
                if obj and self.object_index_is_valid(obj):
                    self.args[argument] = obj
                    continue

            # Try Inventory
            if self.search_scope == SearchScope.Inventory or self.search_scope == SearchScope.Both:
                obj = self.args['player_lifeform'].get_object_by_uuid(arg_uuid)
                if obj and self.object_index_is_valid(obj):
                    self.args[argument] = obj

    def object_index_is_valid(self, obj):
        return not self.SearchTargetMustBeIndexed or self.args['player_lifeform'].item_is_indexed(obj)

    def invalid(self, arg_name):
        return arg_name not in self.args or not self.args[arg_name]

    def execute(self):
        self.process_args()
        return self.perform()

    def perform(self):
        return self.fail()

    def get_uuid_for_argument(self, arg):
        if isinstance(self.args[arg], uuid.UUID):
            return self.args[arg]
        return uuid.UUID(self.args[arg])

    def clean(self, node):
        if node in self.dirtied_characters:
            self.dirtied_characters.remove(node)

    def dirty(self, node):
        if node not in self.dirtied_characters:
            self.dirtied_characters.append(node)

    def append_result(self, uid, result):
        '''Appends a result for a specific uid'''
        if uid not in self.results:
            self.results[uid] = []
        self.results[uid].append(result)

    def append_if_uid(self, obj, result):
        if hasattr(obj, 'uuid'):
            self.append_result(obj.uuid, result)

    def succeed_if_any_results(self, msg_if_failure):
        if len(self.results) > 0:
            return self.succeed()
        return self.fail(msg_if_failure)

    def succeed(self):
        result = CommandResult(True, self, self.results, self.dirtied_characters)
        result.outbox = self.outbox.copy()
        self.sever()
        return result

    def fail(self, result=''):
        failure_messages = {self.player_info.uid: [result]} if result else self.results
        result = CommandResult(False, self, failure_messages, None)
        self.sever()
        return result

    def sever(self):
        self.results = None
        self.context = None

    def specified_coordinates(self):
        if 'coordinates' in self.args:
            coords = self.args['coordinates']
            if isinstance(coords, tuple):
                return coords
            coords = coords.replace('(', '').replace(')', '')
            return tuple([int(x) for x in coords.split(',')])
        return self.args['player_lifeform'].coordinates

    def log(self, lf, result):
        if hasattr(lf, 'uid'):
            self.append_result(lf.uid, result)

    def obs(self, origin, message, acu=0, sen=0, radius=8, exclude=[]):
        observers = list(self.world.actors_in_range(
            origin,
            radius
        ))
        for actor in observers:
            if not isinstance(actor, Lifeform) or actor in exclude:
                continue
            self.log(actor, message)

    def add_to_outbox(self, target, action_message, payload):
        if target.uid not in self.outbox:
            self.outbox[target.uid] = []
        self.outbox[target.uid].append({
            'change': action_message,
            'data': payload
        })
