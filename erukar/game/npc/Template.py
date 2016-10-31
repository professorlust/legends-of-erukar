class Template:
    '''Base class from which all NPC Templates derive'''

    def __init__(self):
        self.conversation_map = {
            'A': ConversationNode('Hello there', ['B', 'C']),
            'A': ConversationNode('Hello there', ['A', 'X']),
            'A': ConversationNode('Hello there', ['X']),
        }

class ConversationNode:
    def __init__(self, dialog, next_nodes):
        self.dialog = dialog
        self.next_nodes = next_nodes
