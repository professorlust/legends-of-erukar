import sys, inspect

class Modules:
    def get_members_of(module):
        for member in inspect.getmembers(sys.modules[module], inspect.isclass):
            yield member

