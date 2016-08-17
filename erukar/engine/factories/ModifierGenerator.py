from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.model.Modifier import Modifier
import inspect

class ModifierGenerator(ModuleDecorator):
    def __init__(self, module, generation_parameters, context):
        self.context = context
        super().__init__(module,generation_parameters)

    def get_possibilities(self):
        for x in inspect.getmembers(self.decoration_module, inspect.isclass):
            if Modifier.can_apply_to(x[1], self.context):
                yield x[1]
