from erukar.engine.model.Direction import Direction
from erukar.engine.commands.CommandResult import CommandResult
import erukar, uuid

class Command:
    OverridesUntilSuccess = False
    not_found = "No object matching '{}' was found in this room."

    def __init__(self):
        '''These parameters are assigned after instantiation'''
        self.player_info = None
        self.world = None
        self.args = {}
        self.dirtied_characters = []
        self.results = {}

    def process_args(self):
        if not self.world: raise
        if not self.args: raise

        self.args['player_lifeform'] = self.player_info.lifeform()

        # Go through all uuids in args and replace with object refs
        for argument in self.args:
            try: arg_uuid = self.get_uuid_for_argument(argument)
            except: continue
            obj = self.world.get_object_by_uuid(arg_uuid)
            if obj: self.args[argument] = obj

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

