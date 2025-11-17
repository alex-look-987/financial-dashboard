def equals(a, b, operator):
    return a >= b if operator == -1 else a <= b

def greater_lower(a, b, operator):
    return a > b if operator == -1 else a < b

def greater_lower_inverted(a, b, operator):
    return a > b if operator == 1 else a < b

def compute(a, b, operator):
    return a - b if operator == -1 else a + b