class CommandResult:
    def __init__(self, success, context, results, indexed, dirtied):
        '''result is a list which contains blocks of texts'''
        self.context = context
        self.results = results
        self.success = success
        self.indexed_items = indexed if indexed else []
        self.dirtied_characters = dirtied if dirtied else []

    def result_for(self, uid):
        if uid in self.results:
            return self.results[uid]
        return []
