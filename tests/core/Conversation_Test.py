import unittest
import erukar
from erukar import Conversation, ConversationBuilder


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
        self.builder = ConversationBuilder()

    def test__basic_validity(self):
        start_str = 'This is the start'
        id, _ = self.builder.add_start(start_str)
        conv = self.builder.conversation
        self.assertIsNotNone(conv.start)
        self.assertEqual(id, conv.start.id)

    def test__add_node__in_builder(self):
        opener = 'Welcome to my shop. There are rats here.'
        choice = 'What would you do about that?'
        response = 'I am not really sure.'
        start_id, _ = self.builder.add_start(opener)
        _id, _ = self.builder.add_node(choice, response, start_id)
        conv = self.builder.conversation
        self.assertIn(_id, conv.start.next)
        # Opener Response
        self.assertEqual(
            opener,
            conv.start.response
        )
        # Choices
        self.assertEqual(
            choice,
            conv.structure[conv.start.next[0]].choice
        )
        # Response
        self.assertEqual(
            response,
            conv.structure[conv.start.next[0]].response
        )

    def test__get_choices(self):
        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        start_id, _ = self.builder.add_start(opener)
        id_1, _ = self.builder.add_node(choice_1, response_1, start_id)
        id_2, _ = self.builder.add_node(choice_2, response_2, start_id)
        choices = list(self.builder.conversation._get_choices(self.player, start_id))
        self.assertEqual(2, len(choices))
        choices = list(self.builder.conversation._get_choices(self.player, id_1))
        self.assertEqual(0, len(choices))

    def test__get_choices_for_player(self):
        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        start_id, _ = self.builder.add_start(opener)
        id_1, _ = self.builder.add_node(choice_1, response_1, start_id)
        id_2, _ = self.builder.add_node(choice_2, response_2, start_id)
        choices = list(self.builder.conversation.get_choices(self.player))
        self.assertEqual(2, len(choices))

    def test__advance(self):
        opener = 'Welcome to my shop. There are rats here.'
        choice_1 = 'What would you do about that?'
        response_1 = 'Response to Choice 1'
        choice_2 = 'Good luck.'
        response_2 = 'Response to Choice 2'
        choice_1_1 = 'Choice against Response 1'
        response_1_1 = 'Response to Choice 1.1'
        start_id, _ = self.builder.add_start(opener)
        id_1, _ = self.builder.add_node(choice_1, response_1, start_id)
        self.builder.add_node(choice_2, response_2, start_id)
        self.builder.add_node(choice_1_1, response_1_1, id_1)
        conv = self.builder.conversation
        choices = conv.advance(self.player, 'asdf')
        self.assertEqual(2, len(choices))
        choices = conv.advance(self.player, choices[0][0])
        self.assertEqual(1, len(choices))
        choices = conv.advance(self.player, choices[0][0])
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
        start_id, _ = self.builder.add_start(opener)
        id_1, _ = self.builder.add_node(choice_1, response_1, start_id)
        self.builder.add_node(choice_2, response_2, start_id)
        self.builder.add_node(choice_1_1, response_1_1, id_1)
        conv = self.builder.conversation
        choices = conv.advance(self.player, 'asdf')
        choices = conv.advance(self.player, choices[0][0])
        choices = conv.advance(self.player, choices[0][0])
        choices = conv.advance(self.player, choices[0][0])
        self.assertNotIn(self.player, [*conv.locations])

    def test__test_conditional_node(self):
        def cond_strong(caller):
            return caller.strength >= 10

        def cond_weak(caller):
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

        start_id, _ = self.builder.add_start(opener)
        id_1, _ = self.builder.add_node(choice_1, response_1, start_id)
        self.builder.add_node(choice_2, response_2, start_id)
        self.builder.add_conditional_node(strong_choice, strong_response, id_1, cond_strong)
        self.builder.add_conditional_node(weak_choice, weak_resposne, id_1, cond_weak)

        conv = self.builder.conversation
        choices = conv.advance(self.player, 'asdf')

        not_strong = conv.advance(self.player, id_1)
        self.assertEqual(weak_choice, not_strong[0][1])

        self.player.strength = 20
        very_strong = conv.advance(self.player, choices[0][0])
        self.assertEqual(strong_choice, very_strong[0][1])
