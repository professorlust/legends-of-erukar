from erukar.system.engine import Conversation


def create(npc):
    conversation = Conversation(npc)
    start_id, _ = conversation.add_start(
        'Welcome to Barlen, home of the Barlen Baker\'s Guild.')
    conversation.add_node(
        text='Who are you?',
        response='I am {}, Local Sheriff of Barlen. If you find bandits or '
        'any sorts of unsavory types, bring me evidence that they have '
        'been "taken care of" and I will reward you nicely.'
        .format(npc.alias()),
        prev_id=start_id)
    what_to_do_id, _ = conversation.add_node(
        text='What is there to do here?',
        response='You can buy all sorts of things here, from weapons and '
        'armor to alchemical potions. If you head out east, you might '
        'stop by the Razorwoods Camp. We are in need of lumber for '
        'construction and you should be able to sell it for a good price.',
        prev_id=start_id)
    where_is_camp_id, _ = conversation.add_node(
        text='Where can I find the Razorwoods Camp?',
        response='The camp is roughly three miles due east. We\'re working '
        'on a road out that way which\'ll head up to Oridel, but that\'s some '
        'time off. Just head east and you can\'t miss it. Make sure to stock '
        'up on supplies before you go; the Razorwoods are a dangerous place.',
        prev_id=what_to_do_id)
    conversation.add_exit(what_to_do_id)
    return conversation
