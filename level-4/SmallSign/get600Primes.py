import math

def is_prime(x):
    if x < 2: return False 
    if x == 2 or x == 3 or x == 5: return True 
    if x % 2 == 0 or x % 3 == 0 or x % 5 == 0: return False 

    prime = 7
    step = 4
    while prime <= math.sqrt(x):
        if x % prime == 0: return False

        prime += step
        step = 6 - step

    return True

def get600primes():
    count = 0
    primes = []
    for i in range(10000):
       if is_prime(i) == True:  
         primes.append(i)
         count = count + 1
         if count == 600:
           return primes

a = get600primes()
print a
