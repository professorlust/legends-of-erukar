from erukar import *
import numpy as np
import unittest

class AttackTests(unittest.TestCase):
    def test_execute_without_match(self):
        p = Player()
        p.uid = 'Bob'
        w = Weapon()
        p.right = w

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        r = Room(None)
        p.link_to_room(r)

        a = Attack()
        a.sender_uid = p.uid
        a.data = data_store
        a.user_specified_payload = "the air"

        result = a.execute()

        self.assertEqual(result.result, Attack.not_found.format("the air"))

    def test_execute_with_match(self):
        p = Player()
        p.uid = 'Bob'
        w = Weapon()
        p.right = w

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        r = Room(None)
        p.link_to_room(r)

        c = Lifeform()
        c.name = "the air"
        c.link_to_room(r)

        a = Attack()
        a.sender_uid = p.uid
        a.data = data_store
        a.user_specified_payload = "the air"

        result = a.execute()

        self.assertTrue("Bob's attack of " in result.result)

    def test_adjudicate_attack_success(self):
        p = Player()
        p.uid = 'Bob'
        p.right = Weapon()

        c = Lifeform()
        c.define_level(1)
        c.name = "the air"

        a = Armor()
        a.armor_class_modifier = -90 # guarantees success
        c.chest = a

        atk = Attack()
        result = atk.adjudicate_attack(p, p.right, c)

        self.assertTrue(' hits ' in result)

    def test_adjudicate_attack_failure(self):
        p = Player()
        p.uid = 'Bob'
        p.right = Weapon()

        c = Lifeform()
        c.define_level(1)
        c.name = "the air"

        a = Armor()
        a.armor_class_modifier = 90 # guarantees failure
        c.chest = a

        atk = Attack()
        result = atk.adjudicate_attack(p, p.right, c)

        self.assertTrue(' misses ' in result)

    def test_adjudicate_attack_cause_dying(self):
        p = Player()
        p.strength =2
        p.uid = 'Bob'
        p.right = Weapon()
        p.right.damages = [Damage('slashing',(10,12),'',(np.random.uniform, (0,1)))]

        c = Lifeform()
        c.health = 1
        c.name = "the air"

        a = Armor()
        a.armor_class_modifier = -90 # guarantees success
        c.chest = a

        atk = Attack()
        result = atk.adjudicate_attack(p, p.right, c)

        self.assertTrue(' has been incapacitated by Bob\'s attack!' in result)
        self.assertTrue(c.afflicted_with(Dying))

    def test_adjudicate_attack_cause_death(self):
        r = Room(None)

        p = Player()
        p.strength = 2
        p.dexterity = 20
        p.uid = 'Bob'
        p.right = Weapon()
        p.link_to_room(r)

        c = Lifeform()
        c.afflictions = [Dying(None)]
        c.name = "the air"
        c.link_to_room(r)

        atk = Attack()
        result = atk.adjudicate_attack(p, p.right, c)

        self.assertTrue(' has been slain by Bob!' in result)
        self.assertTrue(c.afflicted_with(Dead))
        self.assertTrue(c not in r.contents)
