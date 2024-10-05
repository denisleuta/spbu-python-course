from functools import wraps


def curry_explicit(function, arity):
    if arity < 0:
        raise ValueError("Arity will be not is negative")

    def curry_helper(args):
        if len(args) == arity:
            return function(*args)
        if len(args) > arity:
            raise TypeError(f"Expected {arity} arguments, received {len(args)}")
        return lambda x: curry_helper(args + [x])

    if arity == 0:
        return lambda: function()

    return curry_helper([])


def uncurry_explicit(function, arity):
    if arity < 0:
        raise ValueError("Arity will be not is negative")

    @wraps(function)
    def uncurry_helper(*args):
        if len(args) != arity:
            raise TypeError(f"Expected {arity} arguments, received {len(args)}")
        result = function
        for arg in args:
            result = result(arg)
        return result

    return uncurry_helper
