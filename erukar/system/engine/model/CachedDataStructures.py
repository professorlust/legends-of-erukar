class CachedList():
    def __init__(self, generator=None, input_list=None):
        self.inner_list = []
        self.recache(generator, input_list)

    def list(self):
        return self.inner_list

    def invalidate(self):
        self.invalid = True

    def needs_recache(self):
        return self.invalid

    def recache(self, generator=None, input_list=None):
        if generator:
            self.inner_list = list(input_list)
        if input_list:
            self.inner_list = input_list
        self.invalid = False


class CachedSet():
    def __init__(self, generator=None, input_set=None):
        self.inner_set = set()
        self.recache(generator, input_set)

    def set(self):
        return self.inner_set

    def invalidate(self):
        self.invalid = True

    def needs_recache(self):
        return self.invalid

    def recache(self, generator=None, input_set=None):
        if generator:
            self.inner_set = set(input_set)
        if input_set:
            self.inner_set = input_set
        self.invalid = False
