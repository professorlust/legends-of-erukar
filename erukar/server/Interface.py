from erukar.engine.factories.FactoryBase import FactoryBase
from erukar.engine.model.PlayerNode import PlayerNode
from erukar.server.DataAccess import DataAccess
import sys, inspect, erukar, threading

class Interface:
    command_location = 'erukar.engine.commands.executable'
    command_does_not_exist = 'The command \'{0}\' was not found.'

    def __init__(self, shard):
        self.shard = shard
        self.data = DataAccess()
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

    def received_whisper(self, whisper_msg):
        '''received_whisper hook for whenever the node gets a whisper message'''
        # Process the message to get everything you need to generate
        uid = whisper_msg['sender']['uid']
        line = whisper_msg['message']

        return self.execute(uid, line)
    
    def receive(self, uid, line):
        if not any(x.uid == uid for x in self.shard.connected_players):
            self.shard.subscribe(uid)
            return

        if self.shard.is_playing(uid):
            self.execute(uid, line)
            return

        pn = self.shard.get_active_playernode(uid) 
        if pn.status == PlayerNode.RunningScript:
            self.shard.continue_script(pn, line)
            return

        self.append_result(uid, 'Not accepting results') 

    def execute(self, uid, line):
        command, payload = self.command_and_payload(line)
        generation_parameters = {'sender_uid': uid, 'user_specified_payload': payload, 'data': self.data }

        # Now actually make the thing with specified params
        created = self.check_for_aliases(command, generation_parameters)

        # Prevent noninstances from breaking through here
        if created is None or not isinstance(created, erukar.engine.commands.Command):
            generation_parameters['user_specified_payload'] = line
            created = self.factory.create_one('erukar.engine.commands.AmbiguousCommand', generation_parameters)

        # The Command can return something if it needs to for some reason
        instance = self.shard.player_current_instance(uid)
        if instance is not None:
            instance.append(created)

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
            instance.sys_messages.pop()
            instance.remove_player(uid)
            self.shard.transfer_instances(uid)

    def append_result(self, uid, response):
        if uid not in self.messages:
            self.messages[uid] = [response]
            return
        self.messages[uid].append(response)

    def check_for_aliases(self, command, generation_parameters):
        if command not in self.aliases:
            return
        aliased = self.aliases[command]
        target_command = '{0}.{1}'.format(Interface.command_location, aliased.capitalize())
        res = self.factory.create_one(target_command, generation_parameters)
        return res

    def command_and_payload(self, message):
        '''
        Split the received chat message into the first word (will be used to
        create the command object) and the remaining data, which will be used
        as the payload into the instantiated object
        '''
        out = message.split(' ', 1)
        return [out[i] if i < len(out) else '' for i in [0, 1]]
