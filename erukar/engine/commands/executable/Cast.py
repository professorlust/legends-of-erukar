from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.model.Spell import Spell
import erukar, re

class Cast(ActionCommand):
    NoSpell = "No spell '{}' was found in spell book."

    aliases = ['cast']
    TrackedParameters = ['player', 'cast_string', 'target']

    def execute(self):
        player = self.find_player()
        if player is None: return
        self.player = player.lifeform()
        self.room = self.player.current_room

        failure = self.check_for_arguments()
        if failure: return failure

        spell = self.create_spell_chain()

        arguments = {'target': self.target}
        spell.on_cast(self, self.player, arguments)
        return self.succeed()

    def create_spell_chain(self):
        strategem = []
        for word in self.cast_string.split(' '):
            if word.lower() in self.server_properties.SpellWords:
                effect = getattr(erukar.game.magic.effects, self.server_properties.SpellWords[word.lower()])
                strategem.append(effect())
        return Spell('Unknown spell', strategem)

    def check_for_arguments(self):
        if self.context and self.context.should_resolve(self):
            if hasattr(self.context, 'cast_string'):
                self.cast_string = self.context.cast_string
            if hasattr(self.context, 'target'):
                self.target = getattr(self.context, 'target')

            # If we have the parameter and it's not nully, assert that we're done
            if hasattr(self, 'target') and self.target: 
                return

        else:
            target_string = self.find_cast_string_and_target()

            fail = self.resolve_target(target_string)
            if fail: return fail

    def find_cast_string_and_target(self):
        self.cast_string = self.user_specified_payload
        target_string = ''

        for target_preposition in [' at ', ' on ']:
            if target_preposition in self.cast_string:
                self.cast_string, target_string = self.cast_string.split(target_preposition, 1)
                break

        super().resolve_target(target_string)
