from erukar.engine.factories.FactoryBase import FactoryBase
from erukar.server.DataAccess import DataAccess
from multiprocessing import Manager

class Interface:
    command_location = 'erukar.engine.commands.executable'
    command_does_not_exist = 'The command \'{0}\' was not found.'

    def __init__(self):
        self.data = DataAccess()
        self.factory = FactoryBase()
        self.manager = Manager()
        self.requests = self.manager.list([])

    def received_whisper(self, whisper_msg):
        '''received_whisper hook for whenever the node gets a whisper message'''
        # Process the message to get everything you need to generate
        uid = whisper_msg['sender']['uid']
        line = whisper_msg['message']

        return self.execute(uid, line)

    def execute(self, uid, line):
        command, payload = self.command_and_payload(line)
        target_command = '{0}.{1}'.format(Interface.command_location, command.capitalize())
        generation_parameters = {'sender_uid': uid, 'payload': payload, 'data': self.data }

        # Now actually make the thing with specified params
        created = self.factory.create_one(target_command, generation_parameters)
        if created is None:
            return Interface.command_does_not_exist.format(command)

        # The Command tcan return something if it needs to for some reason
        self.requests.append(created)

    def command_and_payload(self, message):
        '''
        Split the received chat message into the first word (will be used to
        create the command object) and the remaining data, which will be used
        as the payload into the instantiated object
        '''
        out = message.split(' ', 1)
        return [out[i] if i < len(out) else '' for i in [0, 1]]
