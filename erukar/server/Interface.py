from erukar.engine.factories.FactoryBase import FactoryBase
from erukar.engine.model.PlayerNode import PlayerNode
import sys, inspect, erukar, threading, json

class Interface:
    command_location = 'erukar.engine.commands.executable'
    command_does_not_exist = 'The command \'{0}\' was not found.'

    def __init__(self, shard):
        self.shard = shard
        self.factory = FactoryBase()
        self.create_alias_list()
        self.messages = {}

    def create_alias_list(self):
        self.aliases = {}
        for name, obj in inspect.getmembers(sys.modules[self.command_location], inspect.isclass):
            if not hasattr(obj, 'aliases'):
                continue
            for a in obj().aliases:
                self.aliases[a] = name

    def receive(self, playernode, line):
        data = json.loads(line)
        target_command = '{0}.{1}'.format(Interface.command_location, data['action'])
        cmd = self.factory.create_one(target_command, None)
        if not cmd: return
        cmd.args = data
        cmd.player_info = playernode
        instance = self.shard.player_current_instance(playernode.uid)
        if instance is not None:
            instance.append(cmd)

    def get_messages_for(self, uid):
        instance = self.shard.player_current_instance(uid)
        messages = self.messages.pop(uid, [])
        if instance is not None:
            messages.extend(instance.get_messages_for(uid))
            self.check_for_transfer(uid, instance)
        return messages

    def check_for_transfer(self, uid, instance):
        '''checks to see if the uid is marked to leave an instance'''
        if uid in instance.sys_messages:
            parameters = instance.sys_messages.pop(uid, [])
            instance.remove_player(uid)
            self.shard.transfer_instances(uid, parameters)

    def append_result(self, uid, response):
        if uid not in self.messages:
            self.messages[uid] = [response]
            return
        self.messages[uid].append(response)

    def check_for_aliases(self, command, generation_parameters):
        if command not in self.aliases:
            return
        aliased = self.aliases[command]
        res = self.factory.create_one(target_command, generation_parameters)
        return res
