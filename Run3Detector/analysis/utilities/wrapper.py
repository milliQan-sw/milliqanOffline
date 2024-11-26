import functools

# defining a decorator  
def mqCut(func, name=None):  
    
    # inner1 is a Wrapper function in   
    # which the argument is called  
        
    # inner function can access the outer local  
    # functions like in this case "func"  
    modified_name = milliqanCuts.func.__name__

    if name!=None:
        modified_name = name
    print("decorator", modified_name)

    @functools.wraps(func)
    def inner1(self, *args, **kwargs):  
        #print("Hello, this is before function execution")  
        # calling the actual function now  
        # inside the wrapper function.  
        wrapped_func = functools.wraps(func, inner1)
        func(self, *args, **kwargs)
        self.cutflowCounter(modified_name)
        print("decorator2", func, modified_name, func.__name__, func.__qualname__)
        #print("This is after function execution")  

    setattr(inner1, '__name__', modified_name)
    inner1.__name__ = modified_name
    return inner1 