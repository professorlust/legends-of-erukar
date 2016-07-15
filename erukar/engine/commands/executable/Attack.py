from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse

class Attack(ActionCommand):
    not_found = "No object matching '{}' was found in this room."
    unsuccessful = "{}'s attack of {} misses {}."
    successful = "{}'s of {} hits {}, dealing {} damage."
    caused_dying = "{}\n{} has been incapacitated by {}'s attack!"
    caused_death = "{}\n{} has been slain by {}!"

    def execute(self):
        player = self.find_player()
        lifeform = self.lifeform(player)
        target = self.find_in_room(lifeform.current_room, self.payload)

        if target is None:
            return Attack.not_found.format(self.payload)
        return self.adjudicate_attack(lifeform, target)

    def adjudicate_attack(self, character, target):
        '''Used to actually resolve an attack roll made between a character and target'''
        target_name = target.alias()
        attack_roll, armor_class, damages = character.attack(target)
        if attack_roll <= armor_class:
            return Attack.unsuccessful.format(character.alias(), attack_roll, target_name)

        damage = sum([x[0] for x in damages])
        damage_descriptions = ', '.join(["{} {}".format(*x) for x in damages])

        attack_string = Attack.successful.format(character.alias(), attack_roll, target_name,
                                                 damage_descriptions)
        target.take_damage(damage)
        if hasattr(target, 'afflictions'):
            if 'dying' in target.afflictions:
                return Attack.caused_dying.format(attack_string, target_name, character.alias())

            if 'dead' in target.afflictions:
                self.create_corpse(target)
                return Attack.caused_death.format(attack_string, target_name, character.alias())

        return attack_string

    def create_corpse(self, target):
        '''Replaces a lifeform with a corpse'''
        room = target.current_room
        room.remove(target)
        room.add(Corpse())
