from erukar.system.engine import ErukarActor

class FactoryBase(ErukarActor):
    def module_and_type(type_to_generate):
        '''
        Split a string like 'erukar.engine.inventory.armor' into
        'erukar.engine.inventory' and 'armor'
        '''
        split_results = type_to_generate.split('.')
        module_name = '.'.join(split_results[:-1])
        type_to_generate = split_results[-1]
        module = __import__(module_name)
        return module, type_to_generate

    def create_template(type_to_generate):
        '''Create a blank template'''
        try:
            module, type_to_generate = FactoryBase.module_and_type(type_to_generate)
        except Exception as msg: return
        # Try to find a type to generate in the module
        if not hasattr(module, type_to_generate):
            return
        return getattr(module, type_to_generate)()

    def create_one(type_to_generate, generation_parameters=None):
        '''
        Create an object template and then use a dictionary to assign values to
        the new object.
        '''
#       try:
        shell = FactoryBase.create_template(type_to_generate)
#       except Error e:
#           print(e)
#           return None

        if generation_parameters:
            for param in [x for x in generation_parameters if hasattr(shell, x)]:
                setattr(shell, param, generation_parameters[param])
        return shell
