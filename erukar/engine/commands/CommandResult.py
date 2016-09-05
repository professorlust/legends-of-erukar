class CommandResult:
    def __init__(self, success, context, result):
        self.context = context
        self.result = result
        self.success = success
