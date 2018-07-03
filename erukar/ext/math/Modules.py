import sys
import inspect


class Modules:
    def get_members_of(module):
        if isinstance(module, list):
            for sub_module in module:
                yield from Modules._members(sub_module)
                return
        yield from Modules._members(module)

    def _members(module):
        for member in inspect.getmembers(sys.modules[module], inspect.isclass):
            yield member
