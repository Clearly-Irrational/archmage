class Item:
    #**kwargs passes keyworded argument(s) to a function
    def __init__(self, use_function=None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs
