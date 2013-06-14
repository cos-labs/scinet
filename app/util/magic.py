"""
"""

@classmethod
def get(cls, key):
    
    # Look up key in registry
    if hasattr(cls, 'registry'):
        return cls.registry.get(key, None)

def regify(klass):
    """ Add subclass registry to class. """
    
    # Add registry to class
    klass.registry = {}
    
    # Add get method to class
    klass.get = get

    # Define metaclass with registry; must be defined within
    # regify() so that klass is included in scope
    class Meta(type):

        def __init__(self, name, bases, dct):
            
            # Call superclass __init__
            type.__init__(self, name, bases, dct)
            
            # Quit if root node
            if self.__name__ == klass.__name__:
                return

            # Clean name
            regname = name.lower()

            # Add class to registry
            self.registry[regname] = self

    # Override class as subclass of Meta
    klass = Meta(
        klass.__name__, 
        klass.__bases__,
        dict(klass.__dict__)
    )

    # Return modified class
    return klass
