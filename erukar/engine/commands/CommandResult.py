class CommandResult:
    def __init__(self, success, context, result, indexed, dirtied):
        '''result is a list which contains blocks of texts'''
        self.context = context
        self.result = result
        self.success = success
        self.indexed_items = indexed if indexed else []
        self.dirtied_characters = dirtied if dirtied else []
