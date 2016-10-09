from erukar.engine.commands.Command import Command
from erukar.engine.model.Damage import Damage
from erukar.engine.environment.Corpse import Corpse
import erukar

class ActionCommand(Command):
    '''Subclass that defines that the command must be used as an action'''
    Deflected = '{target}\'s armor deflected the entirety of the damage from {subject}!'
    EnemyFullMitigation = "{target}'s armor absorbed the entirety of your {weapon_name}'s damage!"
    YourFullMitigation = "Your armor absorbed the entirety of the damage from {target}'s {weapon_name}!"
    CausedDying = "\n{target} has been incapacitated by {subject}'s attack!"
    CausedDeath = "\n{target} has been slain by {subject}!"
    AttackSuccessful = "{subject}'s attack hits {target}, dealing {damage} damage."
    DefaultWeapon = 'unarmed attack'

    def inflict_damage(self, enemy, damages, weapon=None):
        character = self.find_player().lifeform()

        args = {
            'subject': character.alias(),
            'target': enemy.alias(),
            'weapon_name': self.DefaultWeapon if weapon is None else weapon.alias()}

        self.dirty(character)

        # Calculate the actual damage through mitigation and deflection
        for deflected in Damage.deflections(character, enemy, weapon, damages):
            self.append_result(self.sender_uid, self.Deflected.format(**args))
            self.append_result(enemy.uid, self.Deflected.format(**args))

        actuals = list(Damage.actual_damage_values(character, enemy, weapon, damages))

        # Calculate the Damage  
        damage = sum(amt for amt, _ in actuals)
        if damage <= 0:
            self.append_result(self.sender_uid, self.EnemyFullMitigation.format(**args))
            self.append_result(enemy.uid, self.YourFullMitigation.format(**args))
            return

        # Apply the damage
        self.dirty(enemy)
        args['damage'] = ', '.join(["{} {}".format(*x) for x in actuals if x[0] > 0])
        xp = enemy.take_damage(damage, character)
        attack_string = self.AttackSuccessful.format(**args)

        # Check to see if Dying, or Dead.
        if hasattr(enemy, 'afflictions'):
            if enemy.afflicted_with(erukar.engine.effects.Dying):
                attack_string = attack_string + self.CausedDying.format(**args)

            if enemy.afflicted_with(erukar.engine.effects.Dead):
                self.create_corpse(enemy)
                attack_string = attack_string + self.CausedDeath.format(**args)

        # Let everyone know what happened
        self.append_result(self.sender_uid, attack_string)
        self.append_result(enemy.uid, attack_string)

        if xp <= 0: return
        xp_awards = character.award_xp(xp)
        for award in xp_awards:
            self.append_result(self.sender_uid, award)

    def create_corpse(self, target):
        room = target.current_room
        if target in room.contents:
            room.contents.remove(target)
        room.add(Corpse(target))
