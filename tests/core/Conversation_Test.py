import unittest
import erukar
from erukar import Conversation


class Conversation_Test(unittest.TestCase):
    def setUp(self):
        dungeon = erukar.FrameworkDungeon()
        self.interface = erukar.TestInterface(dungeon=dungeon)
        self.interface.dungeon.actors = set()
        self.player = self.interface.player
        self.player.uid = 'test'
        self.basic_data = {
            'player_lifeform': self.player
        }
        dungeon.add_actor(self.player, (0, 0))
        self.player.gain_action_points()
        self.npc = erukar.Npc()
        self.convo = Conversation(self.npc)

    def test__basic_validity(self):
        start_str = 'This is the start'
        id, _ = self.convo.add_start(start_str)
        self.assertIsNotNone(self.convo.start)
        self.assertEqual(id, self.convo.start.id)

    def test__add_node__in_builder(self):
        opener = 'Welcome to my shop. There are rats here.'
        choice = 'What would you do about that?'
        response = 'I am not really sure.'
        start_id, _ = self.convo.add_start(opener)
        _id, _ = self.convo.add_node(choice, response, start_id)
        self.assertIn(_id, self.convo.start.next)
        # Opener Response
        self.assertEqual(
            opener,
            self.convo.start.response
        )
        # Choices
        self.assertEqual(
            choice,
            self.convo.structure[self.convo.start.next[0]].choice
        )
        # Response
        self.assertEqual(
            response,
            self.convo.structure[self.convo.start.next[0]].response
        )

    def test__get_choices(self):
        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        start_id, _ = self.convo.add_start(opener)
        id_1, _ = self.convo.add_node(choice_1, response_1, start_id)
        id_2, _ = self.convo.add_node(choice_2, response_2, start_id)
        choices = list(self.convo._get_choices(self.player, start_id))
        self.assertEqual(2, len(choices))
        choices = list(self.convo._get_choices(self.player, id_1))
        self.assertEqual(0, len(choices))

    def test__get_choices_for_player(self):
        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        start_id, _ = self.convo.add_start(opener)
        id_1, _ = self.convo.add_node(choice_1, response_1, start_id)
        id_2, _ = self.convo.add_node(choice_2, response_2, start_id)
        choices = list(self.convo.get_choices(self.player))
        self.assertEqual(2, len(choices))

    def test__advance(self):
        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        choice_1_1 = 'Choice against Response 1'
        response_1_1 = 'Response to Choice 1.1'
        start_id, _ = self.convo.add_start(opener)
        id_1, _ = self.convo.add_node(choice_1, response_1, start_id)
        self.convo.add_node(choice_2, response_2, start_id)
        self.convo.add_node(choice_1_1, response_1_1, id_1)
        choices = self.convo.advance(self.player, 'asdf')
        self.assertEqual(2, len(choices))
        choices = self.convo.advance(self.player, choices[0][0])
        self.assertEqual(1, len(choices))
        choices = self.convo.advance(self.player, choices[0][0])
        self.assertEqual(1, len(choices))
        self.assertEqual('EXIT', choices[0][1])

    def test__advance_into_exit(self):
        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        choice_1_1 = 'Choice against Response 1'
        response_1_1 = 'Response to Choice 1.1'
        start_id, _ = self.convo.add_start(opener)
        id_1, _ = self.convo.add_node(choice_1, response_1, start_id)
        self.convo.add_node(choice_2, response_2, start_id)
        self.convo.add_node(choice_1_1, response_1_1, id_1)
        choices = self.convo.advance(self.player, 'asdf')
        choices = self.convo.advance(self.player, choices[0][0])
        choices = self.convo.advance(self.player, choices[0][0])
        choices = self.convo.advance(self.player, choices[0][0])
        self.assertNotIn(self.player, [*self.convo.locations])

    def test__test_conditional_node(self):
        def cond_strong(npc, caller):
            return caller.strength >= 10

        def cond_weak(npc, caller):
            return caller.strength < 10

        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        strong_choice = 'I could handle that for you'
        strong_response = 'Oh how strong'
        weak_choice = 'Sorry, good luck with that.'
        weak_resposne = 'Okay.'

        start_id, _ = self.convo.add_start(opener)
        id_1, _ = self.convo.add_node(choice_1, response_1, start_id)
        self.convo.add_node(choice_2, response_2, start_id)
        self.convo.add_node(strong_choice, strong_response, id_1, cond_strong)
        self.convo.add_node(weak_choice, weak_resposne, id_1, cond_weak)

        choices = self.convo.advance(self.player, 'asdf')

        not_strong = self.convo.advance(self.player, id_1)
        self.assertEqual(weak_choice, not_strong[0][1])

        self.player.strength = 20
        very_strong = self.convo.advance(self.player, choices[0][0])
        self.assertEqual(strong_choice, very_strong[0][1])

        self.convo.advance(self.player, 'exit')
        self.assertFalse(self.convo.is_conversing(self.player))

    def test__test_action_node(self):
        def take_sword(npc, caller):
            item = caller.inventory[0]
            caller.inventory.remove(item)
            npc.inventory.append(item)
            return True

        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        sword_choice = 'Take my sword'
        sword_response = 'Thank you!'

        sword = erukar.Longsword()
        self.player.inventory = [sword]

        start_id, _ = self.convo.add_start(opener)
        id_1, _ = self.convo.add_node(choice_1, response_1, start_id)
        self.convo.add_node(choice_2, response_2, start_id)
        self.convo.add_node(sword_choice, sword_response, id_1, action=take_sword)

        choices = self.convo.advance(self.player, 'asdf')
        choices = self.convo.advance(self.player, choices[0][0])
        choices = self.convo.advance(self.player, choices[0][0])

        self.assertNotIn(sword, self.player.inventory)

        self.convo.advance(self.player, 'exit')
        self.assertFalse(self.convo.is_conversing(self.player))

    def test__test_action_condition_node(self):
        def has_sword(npc, caller):
            return caller.find_in_inventory(erukar.Longsword) is not None

        def take_sword(npc, caller):
            sword = caller.find_in_inventory(erukar.Longsword)
            caller.inventory.remove(sword)
            npc.inventory.append(sword)
            return True

        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        sword_choice = 'Take my sword'
        sword_response = 'Thank you!'

        sword = erukar.Longsword()
        self.player.inventory = [sword]

        start_id, _ = self.convo.add_start(opener)
        id_1, _ = self.convo.add_node(choice_1, response_1, start_id)
        self.convo.add_node(choice_2, response_2, start_id)
        self.convo.add_node(
            text=sword_choice,
            response=sword_response,
            prev_id=id_1,
            condition=has_sword,
            action=take_sword)

        choices = self.convo.advance(self.player, 'asdf')
        choices = self.convo.advance(self.player, choices[0][0])
        choices = self.convo.advance(self.player, choices[0][0])

        self.assertNotIn(sword, self.player.inventory)

        self.convo.advance(self.player, 'exit')
        self.assertFalse(self.convo.is_conversing(self.player))
