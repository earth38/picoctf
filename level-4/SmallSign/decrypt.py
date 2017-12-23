# picoctfのサーバにsshでログインしてから実行しないと成功しない
from pwn import *
from get600Primes import * 

lstPrime = get600primes()
#lstPrime = ['''<list of first 600 primes here>''']

test_data = 130

while (True):
    host, port = "shell2017.picoctf.com", 27525
    r = remote(host, port)

    rule = re.compile('[0-9]')
    data = r.readuntil("(-1 to stop):")
    data = rule.findall(data)
    data = "".join(data)
    data = data[2:-6]

    n = int(data)
    lstSign = []

    count = 0

    print "start collecting data"

    try:
        while count<=test_data:

                r.writeline(str(lstPrime[count]))
                #print str(lstPrime[count])
    
                data = r.readuntil("(-1 to stop):")

                #print data

                chal = rule.findall(data)[:-1]
                chal = "".join(chal)
                chal = int(chal)

                lstSign.append(chal)
                count += 1
                #print count
    except:
        print "query out of time"
        test_data -= 10
        print "try smaller test data", test_data
        continue

    print "finish colelcting data"
    r.writeline("-1")

    data = r.readuntil("challenge:")
    print data

    chal = rule.findall(data)
    chal = "".join(chal)
    chal = int(chal)
    print "challenge:", chal

    i = 0
    s = 1
    found = True
    print ""
    while (chal<>1):

        if i>=count:
            print "not found"
            found = False
            break

        if (chal % lstPrime[i] == 0):
            s = s * lstSign[i]
            chal = chal/lstPrime[i]
            print lstPrime[i], lstSign[i]
        else:
            i += 1
            continue

    if (not found):
        r.close()
        print "Cannot find sign of divisor, try again ..."
    else:
        print "N: ", n
        sign = s%n

        print "\n", sign
        r.writeline(str(sign))
        print r.readall()
        break
