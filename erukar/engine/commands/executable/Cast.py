from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.magic.Spell import Spell
import erukar, re

class Cast(ActionCommand):
    NoSpell = "No spell '{}' was found in spell book."

    aliases = ['cast']
    TrackedParameters = ['caster', 'cast_string', 'target']

    def execute(self):
        self.caster = self.find_player().lifeform()
        self.room = self.caster.current_room

        failure = self.check_for_arguments()
        if failure: return failure

        spell, efficacy = self.create_spell_chain()

        return self.attempt_cast(spell, efficacy)

    def attempt_cast(self, spell, efficacy):
        if efficacy < 0.05:
            return self.failed_cast(spell)
        return self.successful_cast(spell, efficacy)

    def successful_cast(self, spell, efficacy):
        arguments = {'target': self.target}
        spell.on_cast(self, self.caster, arguments, efficacy)
        for word in spell.words:
            self.caster.add_successful_cast(word)
        return self.succeed()

    def failed_cast(self, spell):
        print('failed')
        for word in spell.words:
            self.caster.add_failed_cast(word)
        return self.succeed()

    def create_spell_chain(self):
        '''
        Break out the cast_string into different words and assemble a
        chain of spell effects
        '''
        spell_chain = []
        efficacy_from_words = 1.0 

        for word in self.cast_string.split(' '):
            if word.lower() in self.server_properties.SpellWords:
                word_target = self.server_properties.SpellWords[word.lower()]
                effect_class = getattr(erukar.game.magic.words, word_target)
                efficacy_from_words *= self.caster.spell_word_efficacy(word_target)
                spell_chain.append(effect_class())
            else:
                print('could not match ' + word)
        return Spell('Unknown spell', spell_chain), efficacy_from_words

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
        '''Determine if we have specified a target (with 'on' or 'at')'''
        self.cast_string = self.user_specified_payload
        target_string = ''

        for target_preposition in [' at ', ' on ']:
            if target_preposition in self.cast_string:
                self.cast_string, target_string = self.cast_string.split(target_preposition, 1)
                break

        super().resolve_target(target_string)
