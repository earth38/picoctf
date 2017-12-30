from pwn import *
import time
import re

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

def get400primes():
    count = 0
    primes = []
    for i in range(10000):
       if is_prime(i) == True:  
         primes.append(i)
         count = count + 1
         if count == 400:
           return primes

def getSigndata(r,primes):

    try:
        #startTime = time.time()
        data =  r.recvuntil("(-1 to stop):")
       
        #get N and e
        n = data[1][3:]
        data = data.split("\n")
        signs = []

        for i,prime in enumerate(primes):
            r.sendline(str(prime))
            signs.append(r.recvline()[12:].strip())
            r.recvuntil("(-1 to stop):")
            if i == 390:
                r.sendline("-1")
                return signs
    except:
        print "cannot get signatrue..."
        return []


def tryChallenge(r, primes, signs):
    try:
        data =  r.recvline()
        m = re.search(r"[0-9]+$", data)
        sign = int(m.group())

        factors = prime_decomposition(sign)
        answer = 1
        print factors    
        for factor in factors:
            if factor > 2687:
                print "bad..."
                return False

            #print signs
            answer = answer * int(signs[primes.index(factor)])

        r.sendline(str(answer))
        print r.recvall()
        return True
    except:
        print "challenge is failure"
        return False

def prime_decomposition(n):
  i = 2
  table = []
  while i * i <= n:
    while n % i == 0:
      n /= i
      table.append(i)
    i += 1
  if n > 1:
    table.append(n)
  return table



if __name__ == '__main__':
    while True:
        # connect to the Server
        primes = get400primes()
        host, port = 'shell2017.picoctf.com', '27525'
        r = remote(host, port)
      
         # get Signature data per prime
        signs = getSigndata(r, primes)
        
        if not signs:
            continue

        if tryChallenge(r, primes, signs)  :
            break    


