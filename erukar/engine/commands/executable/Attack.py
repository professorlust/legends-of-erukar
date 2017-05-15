from erukar.engine.commands.Command import SearchScope
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.environment.Door import Door
from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Damage import Damage
from erukar.engine.model.AttackState import AttackState
from erukar.engine.formatters.PhysicalDamageFormatter import PhysicalDamageFormatter
from erukar.engine.calculators.Navigator import Navigator
import erukar, random, math

class Attack(ActionCommand):
    NotFound = 'interaction_target not found'
    NoWeapon = 'No Weapon to attack with'
    unsuccessful = "{subject}'s attack of {roll} misses {target}."
    UnableToAttackInDirection = "You are unable to perform a directional attack."
    UnableToAttackInRoom = "You are unable to perform an attack."

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

        new_attack = self.build_attack_state()
        new_attack.efficiency = 1.0
        if isinstance(new_attack.weapon, erukar.engine.inventory.Weapon) and new_attack.weapon.RequiresAmmo:
            new_attack.ammunition = self.args['player_lifeform'].ammunition
        if not new_attack.is_valid():
            return self.fail('Attack state is not valid')
        self.perform_attack(new_attack)

        # Succeed if we have results, otherwise fail with the UnableToAttackInRoom
        return self.succeed_if_any_results(msg_if_failure=self.UnableToAttackInRoom)

    def build_attack_state(self):
        '''Factory method'''
        attack_state = AttackState()
        attack_state.attacker = self.args['player_lifeform']
        attack_state.target   = self.args['interaction_target']
        attack_state.weapon   = self.args['weapon']
        return attack_state

    def perform_attack(self, attack_state):
        '''Used to actually resolve an attack roll made between a character and target'''
        attack_state.calculate_attack()

        if not attack_state.attack_successful():
            PhysicalDamageFormatter.append_missed_attack_results(self, attack_state)
            return

        self.dirty(self.args['player_lifeform'])
        self.dirty(self.args['interaction_target'])

        attack_state.on_process_damage(self)
        attack_state.confirm()
        PhysicalDamageFormatter.process_and_append_damage_result(self, attack_state)

        if attack_state.processed_damage_result.xp_value > 0:
            self.character.award_xp(attack_state.processed_damage_result.xp_value, self)

