from erukar.engine.commands.ActionCommand import ActionCommand

class Say(ActionCommand):
    aliases = ['say', 'talk']

    def execute(self):
        player = self.find_player()
        payload = self.payload()
        room = player.character.current_room

        raw_results = [deco.on_hear(payload, instigator=player.lifeform()) for deco in room.contents]
        results = list(filter(None, raw_results))
        for result in results:
            self.append_result(self.sender_uid, result)
        if len(results) == 0:
            self.append_result(self.sender_uid, 'No one hears you.')
        return self.succeed()
