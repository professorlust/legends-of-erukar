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
        self.copy_tracked_parameters_from(context)

    def resolve_disambiguation(self, parameter):
        '''Used when the new command has a payload that disambiguates'''
        if not self.requires_disambiguation or not parameter:
            return None
        print(self.disambiguating_parameter)
        setattr(self, self.disambiguating_parameter, parameter)

    def copy_tracked_parameters(self, copy_to):
        for tracked in copy_to.TrackedParameters:
            setattr(copy_to, tracked, getattr(self, tracked, None))

    def copy_tracked_parameters_from(self, copy_from):
        for tracked in copy_from.TrackedParameters:
            tracked_value = getattr(copy_from, tracked, None)
            setattr(self, tracked, tracked_value)

    def result_for(self, uid):
        if uid in self.results:
            return self.results[uid]
        return []
