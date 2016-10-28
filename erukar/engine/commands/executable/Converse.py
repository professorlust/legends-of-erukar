from erukar.engine.commands.ActionCommand import ActionCommand
import re

class Converse(ActionCommand):
    aliases = ['say', 'talk']

    def execute(self):
        desired_command, payload = self.check_for_arguments()
        return desired_command(payload)

    def start_conversation(self, target_alias):
        '''Aims to start a dialog with an NPC or other conversable item'''
        player = self.find_player()
        room = player.lifeform().current_room
        target = self.find_in_room(room, target_alias)
        # If there's no target found, just say it out loud
        if not target:
            self.append_result(self.sender_uid, 'Cannot find "{}" in room.'.format(target_alias))
            return self.say_out_loud(target_alias)
        # Starting a conversation with this thing
        self.append_result(self.sender_uid, 'Starting convo with {}'.format(target.alias()))
        return self.succeed()

    def say_out_loud(self, payload):
        player = self.find_player()
        room = player.lifeform().current_room
        raw_results = [deco.on_hear(payload, instigator=player.lifeform()) for deco in room.contents]
        results = list(filter(None, raw_results))
        for result in results:
            self.append_result(self.sender_uid, result)
        if len(results) == 0:
            self.append_result(self.sender_uid, 'No one hears you.')
        return self.succeed()

    def check_for_arguments(self):
        payload = self.payload()
        talk_to = re.findall('^to\s(.*)$', payload)
        if any(talk_to):
            return self.start_conversation, talk_to[0]
        return self.say_out_loud, payload
