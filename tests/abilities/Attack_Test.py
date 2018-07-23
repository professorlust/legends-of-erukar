import unittest
import erukar
from erukar import ActivateAbility, Enemy, Attack
from erukar.ext.math import Shapes
from erukar.content.modifiers.gameplay.unique.MageKiller import MageKiller


class Attack_Test(unittest.TestCase):
    def setUp(self):
        dungeon = erukar.FrameworkDungeon()
        erukar.Room(dungeon, coordinates=Shapes.rect((-2, -2), (2, 2)))
        self.interface = erukar.TestInterface(dungeon=dungeon)
        self.interface.dungeon.actors = set()
        self.player = self.interface.player
        self.player.uid = 'test'
        self.basic_data = {
            'player_lifeform': self.player
        }
        dungeon.add_actor(self.player, (0, 0))
        self.player.gain_action_points()

    def test__valid_at__no_ap(self):
        self.player.consume_action_points(2)
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.assertFalse(Attack().valid_at(cmd, (0, 4)))

    def test__valid_at__no_creature(self):
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.assertFalse(Attack().valid_at(cmd, (0, 4)))

    def test__valid_at__no_weapon(self):
        loc = (0, 4)
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.interface.dungeon.add_actor(Enemy(), loc)
        self.assertTrue(any(cmd.world.creatures_at(self.player, loc)))
        self.assertFalse(Attack().valid_at(cmd, loc))

    def test__valid_at__too_far(self):
        loc = (0, 4)
        self.player.left = erukar.Longsword()
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.interface.dungeon.add_actor(Enemy(), loc)
        self.assertTrue(Attack.has_weapons(self.player))
        self.assertFalse(Attack().valid_at(cmd, loc))

    def test__valid_at__has_weapon(self):
        loc = (0, 1)
        self.player.left = erukar.Longsword()
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.interface.dungeon.add_actor(Enemy(), loc)
        self.assertTrue(Attack.has_weapons(self.player))
        self.assertTrue(Attack().valid_at(cmd, loc))

    def test__has_weapons__is_true_with_left(self):
        self.player.left = erukar.Longsword()
        self.assertTrue(Attack.has_weapons(self.player))

    def test__has_weapons__is_true_with_right(self):
        self.player.right = erukar.Axe()
        self.assertTrue(Attack.has_weapons(self.player))

    def test__has_weapons__is_true_with_both(self):
        self.player.left = erukar.Longsword()
        self.player.right = erukar.Axe()
        self.assertTrue(Attack.has_weapons(self.player))

    def test__action_for_map__yields_none_for_player(self):
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        actions = list(Attack().action_for_map(cmd, (0, 0)))
        self.assertListEqual(actions, [])

    def test__action_for_map__yields_action_appropriately(self):
        loc = (0, 1)
        self.player.right = erukar.Axe()
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        enemy = Enemy()
        self.interface.dungeon.add_actor(enemy, loc)
        actions = list(Attack().action_for_map(cmd, loc))
        self.assertGreater(len(actions), 0)
        self.assertEqual(actions[0]['abilityModule'], Attack.__module__)
        self.assertEqual(actions[0]['command'], 'ActivateAbility')
        self.assertEqual(actions[0]['cost'], 1)
        self.assertEqual(actions[0]['weapon'], str(self.player.right.uuid))
        self.assertEqual(actions[0]['interaction_target'], str(enemy.uuid))

    def test__action_for_map__yields_two_if_two_enemies(self):
        loc = (0, 1)
        self.player.right = erukar.Axe()
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.interface.dungeon.add_actor(Enemy(), loc)
        self.interface.dungeon.add_actor(Enemy(), loc)
        actions = list(Attack().action_for_map(cmd, loc))
        self.assertEqual(len(actions), 2)

    def test__weapons_in_range__yields_only_those_in_range(self):
        self.player.left = erukar.LightCrossbow()
        self.player.right = erukar.Axe()
        weapons = list(Attack.weapons_in_range(self.player, (0, 4)))
        self.assertEqual(len(weapons), 1)
        self.assertEqual(weapons[0], self.player.left)

    def test__valid_weapobs__yields_only_those_in_range(self):
        self.player.left = erukar.LightCrossbow()
        self.player.right = erukar.Axe()
        weapons = list(Attack.valid_weapons(self.player, 4))
        self.assertEqual(len(weapons), 1)
        self.assertEqual(weapons[0], self.player.left)

    def test__check_for_kill__is_valid_for_dying(self):
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        weapon = erukar.LightCrossbow()
        target = Enemy()
        erukar.Dying(target)
        Attack().check_for_kill(cmd, self.player, weapon, target)
        res = Attack.CauseDying.format(target=target.alias())
        self.assertEqual(cmd.results['test'][0], res)

    def test__check_for_kill__is_valid_for_dead(self):
        pre_xp = self.player.experience
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        weapon = erukar.LightCrossbow()
        target = Enemy()
        erukar.Dead(target)
        Attack().check_for_kill(cmd, self.player, weapon, target)
        res = Attack.KillTarget.format(target=target.alias())
        self.assertEqual(cmd.results['test'][0], res)
        self.assertGreater(self.player.experience, pre_xp)

    def test__check_for_kill__is_valid_for_nothing(self):
        pre_xp = self.player.experience
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        weapon = erukar.LightCrossbow()
        target = Enemy()
        Attack().check_for_kill(cmd, self.player, weapon, target)
        Attack.KillTarget.format(target=target.alias())
        self.assertTrue('test' not in cmd.results)
        self.assertEqual(pre_xp, self.player.experience)

    def test__attack_succeeded__fails_if_evasion_is_higher(self):
        def mock_evasion(*_):
            return 100
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        weapon = erukar.LightCrossbow()
        target = Enemy()
        target.evasion = mock_evasion
        res = Attack().attack_succeeded(cmd, self.player, weapon, target, 1)
        self.assertFalse(res)

    def test__attack_succeeded__succeeds_if_roll_is_higher(self):
        def mock_evasion(*_):
            return 1
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        weapon = erukar.LightCrossbow()
        target = Enemy()
        target.evasion = mock_evasion
        res = Attack().attack_succeeded(cmd, self.player, weapon, target, 100)
        self.assertTrue(res)

    def test__is_in_valid_range__fails_if_weapon_range_is_less(self):
        weapon = erukar.LightCrossbow()
        weapon.MaximumRange = 1
        target = Enemy()
        self.interface.dungeon.add_actor(target, (100, 100))
        res = Attack.is_in_valid_range(self.player, weapon, target)
        self.assertFalse(res)

    def test__is_in_valid_range__succeeds_if_weapon_range_is_greater(self):
        weapon = erukar.LightCrossbow()
        weapon.MaximumRange = 100
        target = Enemy()
        self.interface.dungeon.add_actor(target, (0, 1))
        res = Attack.is_in_valid_range(self.player, weapon, target)
        self.assertTrue(res)

    def test__is_in_valid_range__succeeds_if_weapon_range_is_equal(self):
        weapon = erukar.LightCrossbow()
        weapon.MaximumRange = 1
        target = Enemy()
        self.interface.dungeon.add_actor(target, (0, 1))
        res = Attack.is_in_valid_range(self.player, weapon, target)
        self.assertTrue(res)

    def test__has_ammo_if_needed__succeeds_if_weapon_does_not_need_ammo(self):
        weapon = erukar.Longsword()
        res = Attack.has_ammo_if_needed(self.player, weapon)
        self.assertTrue(res)

    def test__has_ammo_if_needed__succeeds_if_weapon_has_ammo(self):
        weapon = erukar.LightCrossbow()
        self.player.ammunition = erukar.CrossbowBolt()
        res = Attack.has_ammo_if_needed(self.player, weapon)
        self.assertTrue(res)

    def test__has_ammo_if_needed__fails_if_cannot_find_any(self):
        weapon = erukar.LightCrossbow()
        res = Attack.has_ammo_if_needed(self.player, weapon)
        self.assertFalse(res)

    def test__weapon_exists__fails_if_it_does_not(self):
        weapon = erukar.LightCrossbow()
        res = Attack.weapon_exists(self.player, weapon)
        self.assertFalse(res)

    def test__weapon_exists__succeeds_if_it_does(self):
        self.player.left = erukar.LightCrossbow()
        res = Attack.weapon_exists(self.player, self.player.left)
        self.assertTrue(res)

    def test__handle_ammo__skips_if_no_ammo_needed(self):
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.player.left = erukar.Longsword()
        ability = Attack()
        ability.possible_modifiers = []
        ability.handle_ammo(cmd, self.player, self.player.left)
        self.assertTrue(self.player.left not in ability.possible_modifiers)

    def test__handle_ammo__adds_if_ammo_present(self):
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.player.left = erukar.LightCrossbow()
        self.player.ammunition = erukar.CrossbowBolt(10)
        ability = Attack()
        ability.possible_modifiers = []
        ability.handle_ammo(cmd, self.player, self.player.left)
        self.assertTrue(self.player.ammunition in ability.possible_modifiers)

    def test__calc_attack_roll__allows_modification(self):
        class _Weapon(erukar.Weapon):
            def __init__(self, *_):
                self.called_modify_roll = False
                self.called_calculate_attack = False

            def modify_element(self, *_):
                self.called_modify_roll = True
                return 50

            def on_calculate_attack(self, *_):
                self.called_calculate_attack = True

            def alias(*_):
                return '__'

        def return_attack_roll(*_):
            return 50
        self.player.calculate_attack_roll = return_attack_roll
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        weapon = _Weapon()
        ability = Attack()
        ability.possible_modifiers = [weapon]
        res = ability.calc_attack_roll(cmd, self.player, weapon, self.player)
        self.assertTrue(weapon.called_calculate_attack)
        self.assertTrue(weapon.called_modify_roll)
        self.assertEqual(res, 50)

    def test__do_damage__does_damage(self):
        def damage_from_attack(*_):
            return {'fire': 10}
        self.player.get_damage_from_attack = damage_from_attack
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        target = Enemy()
        target.health = 20
        ability = Attack()
        ability.possible_modifiers = []
        ability.do_damage(cmd, self.player, erukar.Longsword(), target)
        self.assertEqual(10, target.health)

    def test__final_damages__formats_appropriately(self):
        damages = {'post_mitigation': {
            'fire': 10,
            'ice': 10
        }}
        self.assertEqual(
            Attack.final_damages(damages),
            '10 fire, 10 ice'
        )

    def test__total_mitigation__yields_correctly(self):
        damages = {
            'post_deflection': {
                'fire': 15,
                'ice': 10
            },
            'post_mitigation': {
                'fire': 15,
            }
        }
        mitigations = list(Attack._total_mitigation(damages))
        self.assertEqual(len(mitigations), 1)
        self.assertEqual(
            mitigations[0],
            ('ice', 10)
        )

    def test__partial_mitigation__yields_correctly(self):
        damages = {
            'post_deflection': {
                'fire': 15,
                'ice': 10
            },
            'post_mitigation': {
                'fire': 10,
            }
        }
        mitigations = list(Attack._partial_mitigation(damages))
        self.assertEqual(len(mitigations), 1)
        self.assertEqual(
            mitigations[0],
            ('fire', 5)
        )

    def test__integration__deal_damage(self):
        def validate(*_):
            return None

        def return_attack_roll(*_):
            return 50

        def variance(*_):
            return 10
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.player.calculate_attack_roll = return_attack_roll
        self.player.left = erukar.Longsword()
        self.player.inventory = [self.player.left]
        self.player.left.lower_variance = variance
        self.player.left.upper_variance = variance
        cmd.args['weapon'] = self.player.left
        target = Enemy()
        self.interface.dungeon.add_actor(target, (0, 1))
        cmd.args['interaction_target'] = target
        attack = Attack()
        attack.validate = validate
        res = attack.perform(cmd)
        self.assertEqual(
            res.results['test'][-1][:9],
            'You deal '
        )
        self.assertEqual(
            res.results['test'][-1][-17:],
            ' damage to ERROR!'
        )

    def test__integration__energy_burn_mod_deal_damage(self):
        def validate(*_):
            return None

        def return_attack_roll(*_):
            return 50

        def variance(*_):
            return 10

        def max_arc(*_):
            return 50
        cmd = self.interface.create_command(ActivateAbility, self.basic_data)
        self.player.calculate_attack_roll = return_attack_roll
        self.player.left = erukar.Longsword()
        self.player.inventory = [self.player.left]
        MageKiller().apply_to(self.player.left)
        self.player.left.lower_variance = variance
        self.player.left.upper_variance = variance
        cmd.args['weapon'] = self.player.left
        target = Enemy()
        target.maximum_arcane_energy = max_arc
        target.arcane_energy = 50
        self.interface.dungeon.add_actor(target, (0, 1))
        cmd.args['interaction_target'] = target
        attack = Attack()
        attack.validate = validate
        res = attack.perform(cmd).results['test']
        self.assertEqual(
            res[-1][:9],
            'You deal '
        )
        self.assertEqual(
            res[-1][-17:],
            ' damage to ERROR!'
        )
