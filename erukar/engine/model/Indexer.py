class Indexer:
    def __init__(self):
        '''
        The index tree is a dictionary whose elements belong to the following order:
            { item: [traversal] }

        On the contrary, the reversed tree keeps track of the parent_node for a node:
            { item: parent_node }
        In the event that there is no parent_node (e.g. for Rooms), the parent_node is
        tracked as None in the reversed_tree
        '''
        self.index_tree = {}
        self.reversed_tree = {}

    def index_item(self, item, parent_node):
        '''Used to store to traverse paths through a container tree to find an object'''
        if parent_node not in self.index_tree:
            # Add the parent node as a root node
            self.index_tree[parent_node] = []

        # Add the index to the tree using the traversal path to the parent 
        # node and then appending said node to the end
        self.index_tree[item] = self.index_tree[parent_node] + [parent_node]
        self.reversed_tree[item] = parent_node

    def item_is_indexed(self, item):
        '''Confirm that the item exists within the index_tree'''
        return item in self.item_indexer

    def get_traverse_path_for(self, item):
        '''Get a traverse path from the indexer (if it exists)'''
        if item in self.index_tree:
            return self.index_tree[item]
        return []

    def get_children(self, parent_node):
        '''get all children of a parent node'''
        return [x for x in self.reversed_tree if self.reversed_tree[x] is parent_node]

    def get_parent(self, child):
        return self.reversed_tree.get(child, None)

    def remove_index(self, item):
        '''Remove an item from both trees'''
        if item in self.index_tree:
            self.index_tree.pop(item)
        if item in self.reversed_tree:
            self.reversed_tree.pop(item)
