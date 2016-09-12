from erukar.engine.factories.FactoryBase import FactoryBase
from erukar.server.DataAccess import DataAccess
import sys, inspect

class Interface:
    command_location = 'erukar.engine.commands.executable'
    command_does_not_exist = 'The command \'{0}\' was not found.'

    def __init__(self, shard):
        self.shard = shard
        self.data = DataAccess()
        self.factory = FactoryBase()
        self.create_alias_list()

    def create_alias_list(self):
        self.aliases = {}
        for name, obj in inspect.getmembers(sys.modules[self.command_location], inspect.isclass):
            if not hasattr(obj, 'aliases'):
                continue
            for a in obj().aliases:
                self.aliases[a] = name

    def received_whisper(self, whisper_msg):
        '''received_whisper hook for whenever the node gets a whisper message'''
        # Process the message to get everything you need to generate
        uid = whisper_msg['sender']['uid']
        line = whisper_msg['message']

        return self.execute(uid, line)

    def execute(self, uid, line):
        command, payload = self.command_and_payload(line)
        target_command = '{0}.{1}'.format(Interface.command_location, command.capitalize())
        generation_parameters = {'sender_uid': uid, 'user_specified_payload': payload, 'data': self.data }

        # Now actually make the thing with specified params
        created = self.factory.create_one(target_command, generation_parameters)
        if created is None:
            created = self.check_for_aliases(command, generation_parameters)

        if created is None:
            return Interface.command_does_not_exist.format(command)

        # The Command can return something if it needs to for some reason
        instance = self.shard.player_current_instance(uid)
        if instance is not None:
            instance.append(created)

    def check_for_aliases(self, command, generation_parameters):
        if command not in self.aliases:
            return
        aliased = self.aliases[command]
        target_command = '{0}.{1}'.format(Interface.command_location, aliased.capitalize())
        return self.factory.create_one(target_command, generation_parameters)

    def command_and_payload(self, message):
        '''
        Split the received chat message into the first word (will be used to
        create the command object) and the remaining data, which will be used
        as the payload into the instantiated object
        '''
        out = message.split(' ', 1)
        return [out[i] if i < len(out) else '' for i in [0, 1]]
