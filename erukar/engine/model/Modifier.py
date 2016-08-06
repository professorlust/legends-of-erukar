class Modifier:
    '''Used to alter any RpgEntity'''
    NONE = 0
    NONE_PROHIBITED = 1
    ALL_PERMITTED_BUT_NOT_PROHIBITED = 2
    ALL_PERMITTED = 3
    ALL = 4

    def __init__(self):
        '''Allows explicit permission and explicit prohibition'''
        self.permitted_entities = []
        self.prohibited_entities = []
        self.permission_type = Modifier.ALL

    def modify(self, entity):
        '''Safe-guarded modification entry point'''
        if self.can_apply_to(entity):
            self.apply_to(entity)

    def apply_to(self, entity):
        '''Actually does the modification; this should be overridden'''
        pass

    def can_apply_to(self, entity):
        '''
        Checks to see if this is a valid entity based on entities specified
        in permitted_entities and prohibited_entities and this Modifier's
        permission_type
        '''
        is_permitted = self.is_in_group(entity, self.permitted_entities)
        is_prohibited = any(r for r in self.prohibited_entities if r == type(entity))

        return self.permission_type is Modifier.ALL \
                or (self.permission_type is Modifier.NONE_PROHIBITED and not is_prohibited) \
                or (self.permission_type is Modifier.ALL_PERMITTED_BUT_NOT_PROHIBITED and not is_prohibited and is_permitted) \
                or (self.permission_type is Modifier.ALL_PERMITTED and is_permitted) \
                and not self.permission_type is Modifier.NONE

    def is_in_group(self, entity, group):
        return any(r for r in group if r == type(entity) or issubclass(type(entity), r))
