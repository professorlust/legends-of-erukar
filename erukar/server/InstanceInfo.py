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
    def __init__(self, instance_type=Instance, additional_parameters=None):
        m = Manager()
        if not additional_parameters:
            additional_parameters = {}
        self.instance = instance_type(**additional_parameters)
        self.player_list = []
        self.non_action_commands = m.list([])
        self.action_commands = m.list([])
        self.joins = m.list([])
        self.command_results_list = m.list([])
        self.player_command_contexts = {}

    def append(self, command):
        '''appends the command to the correct queue'''
        if isinstance(command, erukar.engine.commands.executable.Join):
            self.joins.append(command)
            return
        if isinstance(command, erukar.engine.commands.ActionCommand):
            self.action_commands.append(command)
            return
        self.non_action_commands.append(command)
