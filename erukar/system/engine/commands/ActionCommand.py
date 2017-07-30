from erukar.system.engine import Damage, Lifeform, Dead
from .Command import Command

class ActionCommand(Command):
    '''Subclass that defines that the command must be used as an action'''
    Deflected = '{target}\'s armor deflected the entirety of the damage from {subject}!'
    EnemyFullMitigation = "{target}'s armor absorbed the entirety of your {weapon_name}'s damage!"
    YourFullMitigation = "Your armor absorbed the entirety of the damage from {target}'s {weapon_name}!"
    CausedDying = "\n{target} has been incapacitated by {subject}'s attack!"
    CausedDeath = "\n{target} has been slain by {subject}!"
    AttackSuccessful = "{subject}'s attack hits {target}, dealing {damage} damage."
    DefaultWeapon = 'unarmed attack'
    RebuildZonesOnSuccess = True

    def inflict_damage(self, enemy, weapon, efficacy=1.0):
        '''apply a set of damages'''
        if not isinstance(enemy, Lifeform)\
        or enemy.has_condition(Dead):
            return

        character = self.find_player().lifeform()

        self.append_result(self.sender_uid, 'Your {} hits {}!'.format(weapon.alias(), enemy.alias()))
        if hasattr(enemy, 'uid'):
            self.append_result(enemy.uid, '{}\'s {} hits you!'.format(character.alias(), weapon.alias()))

        cumulative_damages = []
        should_incapacitate = False
        for damage in weapon.damages:
            result = self.apply_damage_and_parse_results(enemy, damage, efficacy)
            if result.dealt_damage:
                cumulative_damages.append((result.damage_type, result.damage_amount))

            if result.is_corpsified(enemy):
                self.create_corpse(enemy)
                return

            self.append_and_award_damage_results(result)
            if result.is_incapacitated(enemy):
                should_incapacitate = True
                break

        if len(cumulative_damages) > 0:
            self.append_damage_string(character, enemy, weapon, cumulative_damages)
        if should_incapacitate:
            self.add_incapacitated_strings()

    def apply_damage_and_parse_results(self, enemy, damage, efficacy):
        '''Handles actually applying damage by passing off to RpgEntity'''
        # pass off to enemy to get a DamageResult
        attacker = self.find_lifeform(self.sender_uid)
        damage_result = enemy.apply_damage(damage, attacker, efficacy)
        if damage_result.dealt_damage:
            self.dirty(enemy)
            self.dirty(attacker)
        return damage_result

    def append_and_award_damage_results(self, damage_result):
        # Append all results
        for uid in damage_result.string_results:
            combined = '\n'.join(damage_result.string_results[uid])
            self.append_result(uid, combined)

        #Award All XP
        for uid in damage_result.xp_awards:
            if damage_result.xp_awards[uid] > 0:
                self.find_lifeform(uid).award_xp(damage_result.xp_awards[uid], enemy)
