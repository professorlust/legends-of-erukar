from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.lifeforms.Lifeform import Lifeform

class Attack(ActionCommand):
    not_found = "No object matching '{}' was found in this room."
    unsuccessful = "{subject}'s attack of {roll} misses {target}."
    successful = "{subject}'s attack of {roll} hits {target}, dealing {damage} damage."
    caused_dying = "\n{target} has been incapacitated by {subject}'s attack!"
    caused_death = "\n{target} has been slain by {subject}!"

    def execute(self):
        player = self.find_player()
        lifeform = self.lifeform(player)
        target = self.find_in_room(lifeform.current_room, self.payload)

        direction = self.determine_direction(self.payload.lower())
        if direction is not None:
            return self.attack_in_direction(lifeform, direction)

        if target is None:
            return Attack.not_found.format(self.payload)
        return self.adjudicate_attack(lifeform, target)

    def attack_in_direction(self, player, direction):
        '''Attack randomly in a direction'''
        return 'Attacking ' + direction.name

    def adjudicate_attack(self, subject, enemy):
        '''Used to actually resolve an attack roll made between a character and target'''
        attack_roll, armor_class, damages = self.calculate_attack(subject, enemy)
        damage = sum([x[0] for x in damages])
        damage_descriptions = ', '.join(["{} {}".format(*x) for x in damages])

        args = {
            'subject': subject.alias(), 
            'target': enemy.alias(), 
            'roll': attack_roll, 
            'damage': damage_descriptions}

        if attack_roll <= armor_class:
            return Attack.unsuccessful.format(**args)

        enemy.take_damage(damage)
        attack_string = Attack.successful.format(**args)
        
        if hasattr(enemy, 'afflictions'):
            if 'dying' in enemy.afflictions:
                return attack_string + Attack.caused_dying.format(**args)

            if 'dead' in enemy.afflictions:
                self.create_corpse(enemy)
                return attack_string + Attack.caused_death.format(**args)

        return attack_string

    def create_corpse(self, target):
        '''Replaces a lifeform with a corpse'''
        room = target.current_room
        room.remove(target)
        room.add(Corpse())
    
    def calculate_attack(self, character, target):
        '''Attack another lifeform'''
        armor_class = target.calculate_armor_class()
        if character.weapon is None:
            return [0, armor_class, 0]

        attack_roll = character.roll(character.skill_range('dexterity'))
        damage = character.weapon.roll(character)

        return [attack_roll, armor_class, damage]

