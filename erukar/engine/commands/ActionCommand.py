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

    def inflict_damage(self, enemy, weapon, efficacy=1.0):
        if not isinstance(enemy, erukar.engine.lifeforms.Lifeform)\
        or enemy.has_condition(erukar.engine.conditions.Dead):
            return

        character = self.find_player().lifeform()

        if weapon is None:
            weapon = erukar.engine.inventory.UnarmedStrike()

        self.append_result(self.sender_uid, 'Your {} hits {}!'.format(weapon.alias(), enemy.alias()))
        if hasattr(enemy, 'uid'):
            self.append_result(enemy.uid, 'You are hit by {}\'s {}!'.format(character.alias(), weapon.alias()))

        cumulative_damages = []
        for damage in weapon.damages:
            result = self.apply_damage_and_parse_results(enemy, damage, efficacy)
            if result.dealt_damage:
                cumulative_damages.append((result.damage_type, result.damage_amount))

        if len(cumulative_damages) > 0:
            print(cumulative_damages)
            damage_list = ['{1} {0}'.format(*d) for d in cumulative_damages]
            if len(damage_list) >= 2:
                damage_list[-1] = 'and ' + damage_list[-1]
            if len(damage_list) >= 3:
                damage_list[:-1] = [x + ',' for x in damage_list[:-1]]
            self.append_result(self.sender_uid, 'Your {} does {} damage!'.format(weapon.alias(), ' '.join(damage_list)))
            if hasattr(enemy, 'uid'):
                self.append_result(enemy.uid, '{}\'s {} does {} damage!'.format(character.alias(), weapon.alias(), ' '.join(damage_list)))


    def apply_damage_and_parse_results(self, enemy, damage, efficacy):
        '''Handles actually applying damage by passing off to RpgEntity'''
        # pass off to enemy to get a DamageResult
        damage_result = enemy.apply_damage(damage, self.player.lifeform(), efficacy)
        if damage_result.dealt_damage:
            self.dirty(enemy)
            self.dirty(self.find_lifeform(self.sender_uid))

        # check to see if we're dead
        if damage_result.is_corpsified(enemy):
            self.create_corpse(enemy)
        
        # Append all results
        for uid in damage_result.string_results:
            for res in damage_result.string_results[uid]:
                self.append_result(uid, res)

        #Award All XP
        for uid in damage_result.xp_awards:
            if damage_result.xp_awards[uid] > 0:
                self.find_lifeform(uid).award_xp(damage_result.xp_awards[uid], enemy)
                
        return damage_result


    def create_corpse(self, target):
        room = target.current_room
        if target in room.contents:
            room.contents.remove(target)
        room.add(Corpse(target))
