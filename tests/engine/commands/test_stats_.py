from erukar import *
import unittest, erukar

class StatsTests(unittest.TestCase):
    def test_stats_execute(self):
        d = Dungeon()
        p = Player(d)

        cmd = Stats()
        cmd.world = d
        cmd.player_info = p
        result = cmd.execute() 

        self.assertTrue(result.success)
        
    def test_stats_execute_check_mitigation(self):
        d = Dungeon()
        p = Player(d)
        p.chest = Hauberk()
        erukar.game.modifiers.Steel().apply_to(p.chest)

        cmd = Stats()
        cmd.world = d
        cmd.player_info = p
        result = cmd.execute() 

        slashing_mit = next(x for x in result.result_for(p.uid)[0]['mitigations'] if x['type'] == 'Slashing')
        self.assertTrue(slashing_mit['deflection'] > 0)
        self.assertTrue(result.success)

    def test_stats_execute_check_condition(self):
        d = Dungeon()
        p = Player(d)
        erukar.game.conditions.Ethereal(p)

        cmd = Stats()
        cmd.world = d
        cmd.player_info = p
        result = cmd.execute() 

        self.assertEqual(len(result.result_for(p.uid)[0]['conditions']), 1)
        self.assertTrue(result.success)

    def test_get_mod(self):
        p = Player(None)
        p.strength = 4
        p.right = Sword()

        # Modify any stat value
        ew = erukar.game.modifiers.inventory.weapon.EnhancedWeapon()
        ew.apply_to(p.right)

        result = Stats.get_mod(p, ew.enhancement_type)

        self.assertNotEqual(ew.amount, 0)
        self.assertEqual(result, ew.amount)

    def test_get_mod_no_mod(self):
        p = Player(None)
        p.strength = 4

        result = Stats.get_mod(p, 'strength')

        self.assertEqual(result, 0)
