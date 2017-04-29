from erukar.engine.commands.ActionCommand import ActionCommand


class Give(ActionCommand):
    NotFound = "Take target was not found"
    CannotTake = "'{}' cannot be taken."
    success = "Successfully took {0}"
    LimitToLocal = True

    def cost_to_give(self):
        pass

    def perform(self):
        pass
