from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ErukarBase:
    SimpleMapParams = []

    def get(session):
        pass

    def add_or_update(self, session):
        session.add(self)
        session.commit()

    def copy_from_object(self, existing_object):
        for parameter in self.SimpleMapParams:
            if not hasattr(existing_object, parameter):
                raise Exception('Schema Object attempted to parse a non-existent field on an object: {}'.format(parameter))
            setattr(self, parameter, getattr(existing_object, parameter))

    def create_from_object(existing_object):
        schema = ErukarBase()
        schema.copy_from_object(existing_object) 
        return schema

    def map_schema_to_object(self, existing_object):
        if not existing_object:
            raise Exception('Schema Object attempted to map a null object')
        for parameter in self.SimpleMapParams:
            setattr(existing_object, parameter, getattr(self, parameter))

    def create_from_type(item_type, args=None):
        '''Dynamically create an item from the erukar module'''
        if not item_type: 
            raise Exception("Cannot create from null type")
        prelim_type = item_type.split('.')
        if not args: args = {}
        return getattr(__import__(item_type, fromlist=[prelim_type[-1]]), prelim_type[-1])(**args)
