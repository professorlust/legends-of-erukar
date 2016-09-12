class CommandResult:
    def __init__(self, success, context, result):
        '''result is a list which contains blocks of texts'''
        self.context = context
        self.result = result
        self.success = success
