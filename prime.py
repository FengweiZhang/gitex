def gcd(a,b):
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
