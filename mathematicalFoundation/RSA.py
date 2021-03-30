import random

# 求最大公约数
def gcd(a:int,b:int):
    a,b = abs(a),abs(b)
    if a<b:
        a,b = b,a
    c = a % b
    while c != 0:
        a,b = b,c
        c = a%b
    return b


# 贝祖等式 返回s*A+t*B = (A,B) = r1
def solve_bezout(A:int,B:int):
    s1, s2 = 1, 0
    t1, t2 = 0, 1
    r1, r2 = A, B
    q = 0
    if r2 == 0:
        s, t = s1, t1
    else:
        q = r1//r2
        r1, r2 = r2, -q*r2+r1
        while r2 != 0:
            s1, s2 = s2, -q*s2+s1
            t1, t2 = t2, -q*t2+t1
            q = r1//r2
            r1, r2 = r2, -q*r2+r1
    return(s2,t2,r1) 

# 求解逆元
def get_inverse(a:int,m:int):
    ans = solve_bezout(a,m)[0]
    while ans < 0:
        ans += m
    return ans

# 快速幂算法
def fastPower(base:int,power:int,m:int):
    ans = 1
    while power > 0:
        if power%2 == 1:
            ans = ans * base % m
        power = int(power//2)
        base = (base * base) % m
    return ans



# 判断大整数是否为素数
def is_largePrime(p:int):
    if p%2 == 0:
        return False
    
    k,tmp = 0,p-1
    while tmp%2 == 0:
        k += 1
        tmp = int(tmp//2)
    
    for a in (2,3,5,7,11,13,17,19):
        m_0 =fastPower(a,tmp,p)
        for i in range(k):
            m_1 = fastPower(m_0,2,p)
            if m_1 == 1 and m_0 == -1:
                return False
            m_0 = m_1
    return True

# 大素数生成器
# import random
def largePrime(a:int,b:int):
    flag = True
    while(flag):
        flag = False
        p = random.randint(a,b)
        s = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,\
            101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,\
            211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,\
            307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,\
            401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,\
            503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,\
            601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,\
            701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797)
        for item in s:
            if p % item == 0:
                flag = True
                break
        if not flag and is_largePrime(p):
            return p
            


# 中国剩余定理 Chinese Remainder Theorem
def solve_CRT(B:list,M:list):
    m = 1
    for item in m:
        m *= item
    
    ans = 0
    for i in range(len(M)):
        M_i = int(m//M[i])
        M_i_inverse = get_inverse(M_i,M[i])
        ans += int(B[i] * M_i * M_i_inverse)
    
    ans = ans % m
    return (ans,m)


# RSA加密系统
def RSA_encode(plain:str):
    p,q = largePrime(2**13,2**14-1),largePrime(2**13,2**14-1)
    n, phi = p*q, (p-1)*(q-1)
    e = largePrime(max(p,q),phi) #pq较小时可能有问题
    K_e,K_d = gcd(n,e),get_inverse(e,phi)
    
    group_bits = len(hex(n)[2:])
    cipher = ""
    for i in range(len(plain)):
        pl = ord(plain[i])
        ci = fastPower(pl,e,n)
        cipher += hex(ci)[2:].zfill(group_bits)
    return (cipher,n,e,K_d)

    print(hex(n)[2:])#密文分组位数？

    print(p,q)
    print(n,phi,e)
    print(K_e,K_d)
    print("hello".encode('u'))
    return 0

#RSA解密系统
def RSA_decode(cipher:str,n:int,K_d:int):
    group_bits = int(len(hex(n)[2:]))
    group_num = int(len(cipher)//group_bits)

    plain = ""
    for i in range(group_num):
        ci = int(cipher[i*group_bits:(i+1)*group_bits],16)
        pl = fastPower(ci,K_d,n)
        plain += chr(pl)
    return plain


s = RSA_encode("强大的国家带来繁荣的景象，巴拉巴拉吧小魔仙到处乱飞，明天要去理发")
print(s[0])
print(RSA_decode(s[0],s[1],s[3]))

