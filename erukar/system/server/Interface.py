from erukar.system.engine import FactoryBase, PlayerNode
import sys, inspect

import logging
logger = logging.getLogger('debug')

class Interface:
    command_location = 'erukar.system.engine.commands'
    command_does_not_exist = 'The command \'{0}\' was not found.'

    def __init__(self, shard):
        self.shard = shard
        self.create_alias_list()
        self.messages = {}

    def create_alias_list(self):
        self.aliases = {}
        for name, obj in inspect.getmembers(sys.modules[self.command_location], inspect.isclass):
            if not hasattr(obj, 'aliases'):
                continue
            for a in obj().aliases:
                self.aliases[a] = name

    def receive(self, playernode, data):
        target_command = '{0}.{1}'.format(Interface.command_location, data['command'])
        cmd = FactoryBase.create_one(target_command)
        if not cmd: 
            logger.info('{} not found'.format(target_command))
            return
        cmd.args = data
        cmd.player_info = playernode

        instance = self.shard.player_current_instance(playernode.lifeform())
        if instance: instance.try_execute(playernode, cmd)

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
        res = FactoryBase.create_one(target_command, generation_parameters)
        return res
