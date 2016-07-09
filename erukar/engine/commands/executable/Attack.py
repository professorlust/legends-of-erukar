from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse

class Attack(ActionCommand):
    not_found = "No object matching '{0}' was found in this room."
    unsuccessful = "Your attack of {0} misses {1}."
    successful = "Your attack of {0} hits {1}, dealing {2} damage."
    caused_dying = "{0}\n{1} has been incapacitated by your attack!"
    caused_death = "{0}\n{1} has been slain!"

    def execute(self):
        player = self.find_player()
        target = self.find_in_room(player.character.current_room, self.payload)

        if target is None:
            return Attack.not_found.format(self.payload)
        return self.adjudicate_attack(player.character, target)

    def adjudicate_attack(self, character, target):
        '''Used to actually resolve an attack roll made between a character and target'''
        target_name = target.get_name()
        attack_roll, armor_class, damages = character.attack(target)
        if attack_roll <= armor_class:
            return Attack.unsuccessful.format(attack_roll, target_name)

        damage = sum([x[0] for x in damages])
        damage_descriptions = ', '.join(["{0} {1}".format(x[0], x[1]) for x in damages])

        attack_string = Attack.successful.format(attack_roll, target_name,
                                                 damage_descriptions)
        target.take_damage(damage)
        if hasattr(target, 'afflictions'):
            if 'dying' in target.afflictions:
                return Attack.caused_dying.format(attack_string, target_name)

            if 'dead' in target.afflictions:
                self.create_corpse(target)
                return Attack.caused_death.format(attack_string, target_name)

        return attack_string

    def create_corpse(self, target):
        '''Replaces a lifeform with a corpse'''
        room = target.current_room
        room.remove(target)
        room.add(Corpse())
