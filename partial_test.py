import functools
from flip import flip
def all_must_be_ints(fn):
    @functools.wraps(fn)
    def wrapper(*args,**kwargs):
        if not all(map(lambda x : isinstance(x,int), args)):
            return "All args must be ints"
        return fn(*args,**kwargs)
    return wrapper

@all_must_be_ints
def add(x,y):
    return x+y 

print(add(1,2))
