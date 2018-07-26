import random
import string


class Conversation:
    def __init__(self, owner=None):
        self.owner = owner
        self.structure = {}
        self.locations = {}
        self.start = None

    def get_choices(self, player):
        _id = self.locations.get(player, self.start.id)
        yield from self._get_choices(player, _id)

    def _get_choices(self, player, _id):
        for node in self._node_choices(player, _id):
            yield node.id, node.choice

    def _node_choices(self, player, _id):
        for poss in self.structure[_id].next:
            if self.structure[poss].conditional(player):
                yield self.structure[poss]

    def exit(self, player):
        del self.locations[player]

    def advance(self, player, next_id=''):
        # Need to begin
        if next_id == 'exit':
            self.exit(player)
            return
        if player not in self.locations:
            _id = self.locations.get(player, self.start.id)
            self.locations[player] = _id
        if self.is_valid_choice(player, next_id):
            self.locations[player] = next_id
        choices = list(self.get_choices(player))
        return choices if len(choices) > 0 else [('exit', 'EXIT')]

    def is_valid_choice(self, player, _id):
        choices = list(self.get_choices(player))
        return any(choice[0] == _id for choice in choices)

    def add_start(self, response):
        node = ConversationNode('', response)
        self.start = node
        self.structure[node.id] = node
        return node.out()

    def add_node(self, text, response, prev_id):
        node = ConversationNode(text, response)
        self.structure[node.id] = node
        self.structure[prev_id].add_possibility(node)
        return node.out()

    def add_conditional_node(self, text, response, prev_id, condition):
        node = ConversationNode(text, response)
        self.structure[node.id] = node
        self.structure[prev_id].add_possibility(node)
        node.conditional = condition


class ConversationNode:
    def __init__(self, text, response, possiblities=None):
        self.choice = text
        self.response = response
        self.next = possiblities or []
        self.id = ConversationNode.random_id()

    def conditional(self, caller):
        return True

    def random_id():
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(32))

    def add_possibility(self, branch):
        self.next.append(branch.id)

    def out(self):
        return (self.id, self.next)
