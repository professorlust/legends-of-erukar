from erukar.engine.model.Describable import Describable

class Modifier(Describable):
    NONE = 0
    NONE_PROHIBITED = 1
    ALL_PERMITTED_BUT_NOT_PROHIBITED = 2
    ALL_PERMITTED = 3
    ALL = 4

    Desirability = 0
    PermittedEntities = []
    ProhibitedEntities = []
    PermissionType = ALL
    Persistent = True

    BriefDescription = "{BaseName}"
    AbsoluteMinimalDescription = "Absolute Minimal"
    VisualMinimalDescription = "Visual Minimal"
    VisualIdealDescription = "Visual Ideal"
    VisualRange = (1, 15)
    SensoryMinimalDescription = "Sensory Minimal"
    SensoryIdealDescription = "Sensory Ideal"
    SensoryRange = (6, 20)
    Adjective = "Adjective"
    DetailedMinimalDescription = "{SensoryMinimalDescription} {VisualMinimalDescription}"
    DetailedIdealDescription = "{SensoryIdealDescription} {VisualIdealDescription}"

    def __init__(self):
        super().__init__()
        self.set_vision_results(self.VisualMinimalDescription, self.VisualIdealDescription, self.VisualRange)
        self.set_sensory_results(self.SensoryMinimalDescription, self.SensoryIdealDescription, self.SensoryRange)
        self.set_detailed_results(self.DetailedMinimalDescription, self.DetailedIdealDescription)

    def modify(self, entity):
        '''Safe-guarded modification entry point'''
        if self.can_apply_to(entity):
            self.apply_to(entity)

    def apply_to(self, entity):
        '''Actually does the modification; this should be overridden'''
        pass

    def on_start(self, room):
        pass

    def on_take(self, lifeform):
        pass

    def on_drop(self, room, lifeform):
        pass

    def on_move(self, room):
        pass

    def on_equip(self, lifeform):
        pass

    def on_unequip(self, lifeform):
        pass

    def can_apply_to(self, entity):
        '''
        Checks to see if this is a valid entity based on entities specified
        in PermittedEntities and ProhibitedEntities and this Modifier's
        PermissionType
        '''
        is_permitted = Modifier.is_in_group(self, entity, self.PermittedEntities)
        is_prohibited = any(r for r in self.ProhibitedEntities if r == type(entity))

        return self.PermissionType is Modifier.ALL \
                or (self.PermissionType is Modifier.NONE_PROHIBITED and not is_prohibited) \
                or (self.PermissionType is Modifier.ALL_PERMITTED_BUT_NOT_PROHIBITED\
                    and not is_prohibited and is_permitted) \
                or (self.PermissionType is Modifier.ALL_PERMITTED and is_permitted) \
                and not self.PermissionType is Modifier.NONE

    def is_in_group(self, entity, group):
        '''
        Used to determine if the entity belongs to either the Permitted or 
        the Prohibited Entities Lists
        '''
        return any(r for r in group if isinstance(entity, r))

