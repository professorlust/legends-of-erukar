class MagicEffect:
    def enact(self, instigator, target, **kwargs):
        pass

    def arg(name, default, type, **kwargs):
        if name in kwargs and isinstance(kwargs[name], type):
            return kwargs[name]
        return default
