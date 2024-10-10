def upperdeco(function):
    def wrapper(a1, a2):
        f = function(a1, a2)
        upper = f.upper()
        return upper
    return wrapper

@upperdeco
def say_hi(int1, int2):
    return f"Hello world! at {int1} and {int2}"

print(f"Lower say_hi()={say_hi(56, 43)}")