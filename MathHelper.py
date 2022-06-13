
# Adds vector 'b' to vector 'a'
def add_vectors(a = (0,0), b = (0,0)):
    if type(a) == tuple and type(b) == tuple:
        return (a[0] + b[0], a[1] + b[1])
    else:
        return "failed, wrong type"

# Subtracts vector 'bä from vector 'a'
def subtract_vectors(a = (0,0), b = (0,0)):
    if type(a) == tuple and type(b) == tuple:
        return (a[0] - b[0], a[1] - b[1])
    else:
        return "failed, wrong type"

# Multiplies two vectors.
def multiply_vectors(a = (0,0), b = (0,0)):
    if type(a) == tuple and type(b) == tuple:
        return (a[0] * b[0], a[1] * b[1])
    else:
         return "failed, wrong type"

# Multiplies vector with a number.
def multiply_vector(a = (0,0), b = 0):
    return (a[0] * b, a[1] * b)

# Divides vector by a number
def divide_vector(a = (0,0), b = 0):
    div_amount = 1/b
    return multiply_vector(div_amount)

# Divides vector 'a' by vector 'b'.
def divide_vectors(a = (0,0), b= (0,0)):
    div_x = 1/b[0]
    div_y = 1/b[1]
    return multiply_vectors(a, (div_x, div_y))

    