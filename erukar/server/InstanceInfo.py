from erukar.server.Instance import Instance
from erukar.server.Interface import Interface
from multiprocessing import Manager
import erukar

class InstanceInfo:
    '''
    Small object which exists on the main thread that keeps track
    of information that the Shard should know about a Dungeon
    Instance, e.g. PlayerList, command_queue, command results list
    '''
    def __init__(self, instance_type=Instance, props=None, additional_parameters=None):
        self.setup_instance(instance_type, props, additional_parameters)
        self.setup_lists()
        self.waiters = []

    def setup_instance(self, instance_type, props, additional_parameters):
        if not additional_parameters:
            additional_parameters = {}
        self.instance = instance_type(**additional_parameters)
        self.instance.info = self
        self.instance.properties = props 
        self.identifier = self.instance.identifier

    def setup_lists(self):
        self.manager = Manager()
        self.non_action_commands = self.manager.list([])
        self.action_commands = self.manager.list([])
        self.responses = self.manager.dict([])
        self.sys_messages = self.manager.dict([])
        self.player_command_contexts = {}
        self.player_list = self.manager.list([])

    def player_join(self, uid):
        if self.instance.is_ready:
            self.do_join(uid)
        else: self.waiters.append(uid)

    def do_join(self, uid):
        self.player_list.append(uid)
        self.instance.subscribe(uid)

    def on_instance_ready(self):
        for waiter in self.waiters:
            self.do_join(waiter)

    def remove_player(self, uid):
        self.player_list[:] = [u for u in self.player_list if u != uid]

    def append(self, command):
        '''appends the command to the correct queue'''
        if isinstance(command, erukar.engine.commands.ActionCommand):
            self.action_commands.append(command)
            return
        self.non_action_commands.append(command)

    def get_messages_for(self, uid):
        return self.responses.pop(uid, [])
