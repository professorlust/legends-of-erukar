class InitializationException(Exception):
    def __init__(self, module):
        super().__init__( 'The decorator for "{}" has not been initialized.'.format(module.__name__))
