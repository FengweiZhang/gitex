# import math

def gcd(a,b):
    a = abs(a)
    b = abs(b)
    if b == 0:
        return a  
    else :
        return gcd(b,a%b)
        

def is_prime (n):
    n = int(n)
    upper = int(n ** 0.5)
    # print(type(upper))
    upper += 1
    for i in range(2,upper):
        if n % i == 0 :
            return False
    return True


def get_prime (N):
    a = [True] * (N + 1)
    indices = list(range(2,N + 1))
    for index in indices:
        if not a[index]:
            pass 
        else :
            i = 2
            while index * i <= N :
                a[i * index] = False 
                i += 1
    ans = list(filter(lambda x:a[x],indices))
    return ans


def bezout(a,b):
    s2 = 0
    s1 = 1
    t2 = 1
    t1 = 0
    q = int(a / b)
    r2 = a % b
    r1 = b

    while r2 != 0:
        s2,s1 = -q * s2 + s1 , s2
        t2,t1 = -q * t2 + t1 , t2
        q = int(r1 / r2)
        r2,r1 = -q * r2 + r1 , r2
    return (s2,t2)

# 求多个整数的gcd gcd_n(12,32,45,64)
def gcd_n(*a):
    if len(a) == 2:
        return gcd(a[0],a[1])
    else:
        d = gcd(a[0],a[1])
        for i in range(2,len(a)):
            d = gcd(d,a[i])
            if d == 1:
                return d
        return d
