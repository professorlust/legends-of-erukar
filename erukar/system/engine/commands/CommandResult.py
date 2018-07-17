class CommandResult:
    def __init__(self, success, context, results, dirtied):
        '''result is a list which contains blocks of texts'''
        self.context = context
        self.results = results
        self.success = success
        self.dirtied_characters = dirtied if dirtied else []
        self.outbox = {}

    def result_for(self, uid):
        if uid in self.results:
            return self.results[uid]
        return []
