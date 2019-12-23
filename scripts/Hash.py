import random

def hashFunction(content):
    return hash(content)

def hashFunction2(content):
    hash = 0
    for i in range(len(content)):
        hash = 37 * hash + ord(content[i])
    return hash
    
def getRandomValues(num, max):
    values = []
    for i in range(num):
        values.append(random.randint(1, max))
    return values

def getRandomValues(num, max):
    values = []
    for i in range(num):
        values.append(random.randint(1, max))
    return values

def getRandomValuesDifferentFromArray(array, max):
    values = []
    for i in range(len(array)):
        aux = random.randint(1, max)
        if array[i] != aux:
            values.append(aux)
        else:
            i -= 1
    return values