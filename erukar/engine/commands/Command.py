from erukar.engine.model.Direction import Direction
from erukar.engine.commands.CommandResult import CommandResult
import erukar, uuid
from enum import Enum

class SearchScope(Enum):
    World = 0
    Inventory = 1
    Both = 2

class Command:
    SearchTargetMustBeIndexed = False
    LimitToLocal = False
    NeedsArgs = True

    def __init__(self):
        '''These parameters are assigned after instantiation'''
        self.search_scope = SearchScope.World
        self.player_info = None
        self.world = None
        self.args = {}
        self.dirtied_characters = []
        self.results = {}

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

    def execute(self):
        self.process_args()
        return self.perform()

    def perform(self):
        return self.fail()

    def get_uuid_for_argument(self, arg):
        if isinstance(self.args[arg], uuid.UUID):
            return self.args[arg]
        return uuid.UUID(self.args[arg])

    def clean(self, lifeform):
        if lifeform in self.dirtied_characters:
            self.dirtied_characters.remove(lifeform)

    def dirty(self, lifeform):
        if lifeform not in self.dirtied_characters:
            self.dirtied_characters.append(lifeform)

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
        self.sever()
        return result

    def fail(self, result=''):
        failure_messages = {self.player_info.uuid: [result]} if result else self.results
        result = CommandResult(False, self, failure_messages, None)
        self.sever()
        return result

    def sever(self):
        self.results = None
        self.context = None

