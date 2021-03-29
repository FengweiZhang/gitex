# import math
import numpy as np 
import random 


# =====================================================================================
# 注释掉两条分割线之间的东西来使用
import torch
from torch import nn
import pandas as pd



def shape_conv(h,h_k,stride,padding):
    return int((h - h_k + stride + 2 * padding) / stride)

def shape_trans_conv(h,h_k,stride,padding,out_padding=0):
    """
        H_out = (H_in - 1)*stride - 2*padding + kernel_size + out_padding
        If we choose stride = 2,kernel_size = 2 and both padding are 0
        Then the H and W are doubled
    """
    return int(
        (h - 1) * stride - 2 * padding + h_k + out_padding
    )


def draw_table(m,mode):
    """
    mode = 'add' or 'mul'
    """

    sheet = np.zeros((m,m))
    if mode == 'add':
        for i in range(m):
            for j in range(m):
                sheet[i,j] = (i + j) % m
    else:
        for i in range(m):
            for j in range(m):
                sheet[i,j] = (i * j) % m

    ans = pd.DataFrame(sheet)
    ans.to_excel(f'm={m}_mode={mode}.xlsx')

class PixelNorm(nn.Module):
    def __init__(self):
        super(PixelNorm,self).__init__()
    
    def forward(self,X):
        tmp = X * X
        return X / torch.sqrt(tmp.sum(dim=1,keepdim=True))

class Maxout(nn.Module):
    def __init__(self,num_in,num_out,pieces):
        super(Maxout,self).__init__()
        self.W = nn.Parameter(torch.randn(num_in,num_out,pieces))
        self.b = nn.Parameter(torch.randn(num_out,pieces))
    def forward(self,X):
        return torch.from_numpy(np.max(np.tensordot(X.detach().numpy(),self.W.detach().numpy(),axes=1) + self.b.detach().numpy(),axis=2))

# =====================================================================================


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
    '''
    求多个整数的gcd gcd_n(12,32,45,64)
    '''
    if len(a) == 2:
        return gcd(a[0],a[1])
    else:
        d = gcd(a[0],a[1])
        for i in range(2,len(a)):
            d = gcd(d,a[i])
            if d == 1:
                return d
        return d


def get_inverse(a,m):
    tmp = bezout(a,m)[0]
    while tmp <= 0:
        tmp += m
    return tmp
# draw_table(30,'mul')


def china_res(b:list,m:list):
    '''
    the first element of returned tuple is the ANS
    the second element of returned tuple is the product of M_i
    '''
    M = 1
    for item in m:
        M *= item
    
    ans = 0
    
    for i in range(len(m)):
        m_i = m[i]
        M_i = int(M / m_i)
        M_i_inverse = get_inverse(M_i,m_i)
        ans += int(b[i] * M_i * M_i_inverse)
    
    while (ans-M) > 0:
        ans -= M

    return (ans,M)



def euler(n:int):
    N = n
    primes = get_prime(n)
    p_set = []
    for p in primes:
        while n % p == 0:
            n /= p
            p_set.append(p)
    p_set = set(p_set)
    ans = N
    for p in p_set:
        ans *= (1 - 1/p)
    return int(ans)


def solve_foce(a:int,b:int,m:int):
    '''
    solve_first_order_congruence_equation
    return value is a tuple
    the first element of tuple is constant
    the second element of tuple is the coefficient of t
    '''
    gcd_a_m = gcd(a,m)
    a1 = get_inverse(int(a/gcd_a_m), int(m/gcd_a_m))
    a2 = b / gcd_a_m * a1
    a2 = int(a2)
    return (a2,int(m/gcd_a_m))

def calc(a,m):
    '''
    Calc a % m
    '''
    pass


# def mod_exp(b,n,m):
#     '''
#     calc b^n % m
#     '''
#     b1 = b
#     n1 = n
#     m1 = m

#     n = bin(n)
#     n = n[2:]
#     n = n[::-1]

#     a = 1
#     for item in n:
#         a = (a * (b **int(item))) % m
#         b = b**2
#     return a
#     pass

def m2m(m,e,b):
    '''
    return m^e % b
    '''
    result=1
    m1=m
    while(e>=1):
        e1=e%2
        if(e1==1):
            result=(m1*result)%b
        m1=(m1**2)%b
        e=e//2
    # print(int(result))
    return int(result)

class RSA():
    def __init__(self,p=19260817,q=19260817):
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (self.p -1) * (self.q -1)
        self.e = random.randint(2,self.phi)
        while gcd(self.e,self.phi) != 1:
            self.e = random.randint(2,self.phi)
        self.d = get_inverse(self.e,self.phi)
        # print(self.p,self.q,self.e)
    
    def lock(self,m):
        # c = m ** self.e % self.n
        c = m2m(m,self.e,self.n)
        return c

    def unlock(self,c):
        m = m2m(c,self.d,self.n)
        return m


    




if __name__ == '__main__':
    # print(get_prime(17))
    # print(euler(18)
    m = 121
    p = 6133
    q = 6143
    print(f'm is {m}')

    r = RSA(p,q)
    c = r.lock(m)
    print(f'c is {c}')
    m = r.unlock(c)
    print(f'm is {m}')
    # p = 6133
    # q = 6143
    # n = p * q
    # print(bin(n))
    # c = 10697729
    # mod_exp()



    # print(mod_exp(468,237,667))
    # m = [9,11,101]
    # b = [1,1,1]
    # M = 1
    # for m_i in m:
    #     M *= m_i
    
    # for m_i in m:
    #     print(m_i,get_inverse(m_i,M))
    # # a = 330
    # m = 7
    # print(get_inverse(a,m))

    # b = [1,5,4,10]
    # m = [5,6,7,11]
    # print(china_res(b,m))

    # b = [2,3,2]
    # m = [3,5,7]
    # print(china_res(b,m))