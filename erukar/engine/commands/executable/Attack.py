from erukar.engine.commands.Command import SearchScope
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.environment.Door import Door
from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Damage import Damage
from erukar.engine.inventory.Weapon import Weapon
from erukar.engine.calculators.Navigator import Navigator
from erukar.engine.conditions import *
import erukar, random, math

class Attack(ActionCommand):
    NotFound = 'interaction_target not found'
    NoWeapon = 'No Weapon to attack with'
    unsuccessful = "{subject}'s attack of {roll} misses {target}."
    UnableToAttackInDirection = "You are unable to perform a directional attack."
    UnableToAttackInRoom = "You are unable to perform an attack."
    
    RebuildZonesOnSuccess = True

    '''
    Requires:
        interaction_target
        weapon
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Both

    def cost_to_attack(self):
        '''This will scale with weapon mass and strength as well as with aerodynamicity and dexterity'''
        return 1

    def perform(self):
        '''Attack an enemy within the current room'''
        # Attack with each weapon, keeping track of the penalties for dual wielding each time
        if 'interaction_target' not in self.args or not self.args['interaction_target']: return self.fail(Attack.NotFound)
        if 'weapon' not in self.args or not self.args['weapon']: return self.fail(Attack.NoWeapon)

        cost = self.cost_to_attack()
        if self.args['player_lifeform'].action_points() < cost:
            return self.fail('Not enough action points!')
        self.args['player_lifeform'].consume_action_points(cost)

        if not self.weapon_exists():
            return self.fail('Cannot Attack -- Weapon is invalid')
        failed_requirements = self.args['weapon'].failing_requirements(self.args['player_lifeform'])
        if failed_requirements:
            return self.fail('. '.join(failed_requirements))
        if not self.has_ammo_if_needed():
            return self.fail('The appropriate ammo for this weapon is not equipped!')
        if not self.is_in_valid_range():
            return self.fail('Target is outside of maximum range!')

        return self.perform_attack()

    def perform_attack(self):
        '''Used to actually resolve an attack roll made between a character and target'''
        attack_roll = self.calculate_attack()

        final_attack_roll, did_hit = self.check_for_hit(attack_roll)
        if not did_hit: return self.succeed()

        self.dirty(self.args['player_lifeform'])
        self.dirty(self.args['interaction_target'])

        self.execute_damage_application_sequence(final_attack_roll)

        return self.succeed()

    def execute_damage_application_sequence(self, final_attack_roll):
        '''Runs through the application and reduction sequence'''
        raw_damage = self.process_raw_damage(final_attack_roll)
        post_deflection_damage = self.process_deflections(raw_damage)
        final_damages = self.process_mitigations(post_deflection_damage)
        self.do_damage_application(final_damages)
        self.check_for_killed_enemy()

    def process_raw_damage(self, final_attack_roll):
        damages = self.args['player_lifeform'].on_successful_hit(self.args['interaction_target'], self.args['weapon'], final_attack_roll)
        #self.add_raw_damage_commentary(damages, final_attack_roll)
        return damages
        
    def process_deflections(self, damages):
        post_deflection_damage = self.args['interaction_target'].apply_deflection(self.args['player_lifeform'], self.args['weapon'], damages)
        #self.add_deflected_damage_commentary(post_deflection_damage)
        return post_deflection_damage

    def process_mitigations(self, damages):
        final_damages = self.args['interaction_target'].apply_mitigation(self.args['player_lifeform'], self.args['weapon'], damages)
        #self.add_final_damage_commentary(final_damages)
        return final_damages 

    def do_damage_application(self, final_damages):
        damage_str = ', '.join('{} {}'.format(*x) for x in final_damages)
        attacker_str = self.args['player_lifeform'].alias()
        defender_str = self.args['interaction_target'].alias()
        self.args['interaction_target'].apply_damage(self.args['player_lifeform'], self.args['weapon'], final_damages)
        self.append_result(self.player_info.uid, 'You have dealt {} damage to {}!'.format(damage_str, defender_str))
        self.append_result(self.args['interaction_target'].uid, '{} has dealt {} damage to you!'.format(attacker_str, damage_str))

    def check_for_killed_enemy(self):
        if self.args['interaction_target'].has_condition(Dying):
            self.append_result(self.player_info.uid, '{} is dying!'.format(self.args['interaction_target'].alias()))
            return
        if self.args['interaction_target'].has_condition(Dead):
            self.world.remove_actor(self.args['interaction_target'])
            corpse = self.args['interaction_target']
            self.world.add_actor(corpse, self.args['interaction_target'].coordinates)
            xp = self.args['interaction_target'].calculate_xp_worth()
            self.args['player_lifeform'].award_xp(xp, self)
            self.append_result(self.player_info.uid, '{} has been slain!'.format(self.args['interaction_target'].alias()))
            self.append_result(self.args['interaction_target'].uid, 'You have been slain by {}...'.format(self.args['player_lifeform'].alias()))

    def weapon_exists(self):
        '''Is the weapon real and valid?'''
        return self.args['weapon'] and isinstance(self.args['weapon'], Weapon)

    def is_in_valid_range(self):
        '''Is the distance between us and the target within the maximum range?'''
        dist = Navigator.distance(self.args['player_lifeform'].coordinates, self.args['interaction_target'].coordinates)
        return dist <= self.args['weapon'].MaximumRange

    def has_ammo_if_needed(self):
        '''Do we consume ammo and have the right ammo?'''
        return not self.args['weapon'].RequiresAmmo or self.args['weapon'].has_correct_ammo(self.args['player_lifeform'].ammunition)

    def calculate_attack(self):
        self.args['weapon'].on_calculate_attack(self)
        base_attack_roll = self.args['player_lifeform'].calculate_attack_roll(1.0, self.args['interaction_target'])
        modified_attack_roll = self.args['weapon'].on_calculate_attack_roll(base_attack_roll, self.args['player_lifeform'], self.args['interaction_target'])

        self.append_result(self.player_info.uid, 'Your attack roll is {} (base: {})'.format(base_attack_roll, modified_attack_roll))
        self.append_result(self.args['interaction_target'].uid, 'The enemy\'s attack roll is {} (base: {})'.format(base_attack_roll, modified_attack_roll))

        return modified_attack_roll

    def check_for_hit(self, attack_roll):
        modified_attack_roll = self.args['interaction_target'].on_check_for_hit(self.args['player_lifeform'], self.args['weapon'], attack_roll)
        if modified_attack_roll <= self.args['interaction_target'].evasion():
            # Events for both target and attacker
            self.args['interaction_target'].on_successful_dodge(self.args['player_lifeform'], self.args['weapon'], modified_attack_roll)
            self.args['player_lifeform'].on_missed_hit(self.args['interaction_target'], self.args['weapon'], modified_attack_roll)

            self.append_result(self.player_info.uid, '{} dodged out of the way of your attack ({} evasion)!'.format(self.args['interaction_target'].alias(), self.args['interaction_target'].evasion()))
            self.append_result(self.args['interaction_target'].uid, 'You dodge out of the way of {}\'s attack!'.format(self.args['player_lifeform'].alias()))
            return 0, False

        self.args['interaction_target'].on_failed_dodge(self.args['player_lifeform'], self.args['weapon'], modified_attack_roll)
        self.args['player_lifeform'].on_successful_hit(self.args['interaction_target'], self.args['weapon'], modified_attack_roll)
        return modified_attack_roll, True

    def attacker_args(self, damages):
        return damages, self.args['interaction_target'], self.args['weapon']
