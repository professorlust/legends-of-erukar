class CommandResult:
    def __init__(self, success, context, results, indexed, dirtied):
        '''result is a list which contains blocks of texts'''
        self.context = context
        self.results = results
        self.success = success
        self.indexed_items = indexed if indexed else []
        self.dirtied_characters = dirtied if dirtied else []
        self.disambiguating_parameter = ''
        self.requires_disambiguation = False

    def resolve_disambiguation(self, parameter):
        '''Used when the new command has a payload that disambiguates'''
        if not self.requires_disambiguation or not parameter:
            return None
        setattr(self, self.disambiguating_parameter, self.indexed_items[parameter])

    def copy_tracked_parameters(self, copy_to):
        for tracked in copy_to.TrackedParameters:
            setattr(copy_to, tracked, getattr(self, tracked))

    def result_for(self, uid):
        if uid in self.results:
            return self.results[uid]
        return []
