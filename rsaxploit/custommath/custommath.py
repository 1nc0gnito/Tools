# Useful Mathematical algorithms

def is_perfect_sqr(n):
    h = n & 0xF
    if h > 9:
        return -1

    if (h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8):
        x = get_sqrt(n)
        if x**2 == n:
            return x
        else:
            return -1
    return -1

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
        print factors
    if n > 1:
        factors.append(n)
    return factors

def get_sqrt(n):
    if n < 0:
        raise ValueError('Square Root not define for negative numbers')
    if n == 0:
        return n
    a,b = divmod(bitlenght(n), 2)
    x = 2**(a + b)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y

def bitlenght(n):
    assert n >= 0
    x = 0
    while n > 0:
        x += 1
        n >>= 1
    return x

def mod_inv(a, b):
    g, x, y = xgcd(a, b)
    if g == 1:
        return x % b
    else:
        return None
####################################### Continued Fractions ###################################
def rational_to_contfrac(x, y):
    a = x // y
    p_quotients = [a]
    while a * y != x:
        x,y = y, x - a * y
        a = x // y
        p_quotients.append(a)
    return p_quotients

def convergents_from_contfrac(frac):
    convergents = []
    for i in range(len(frac)):
        convergents.append(contfrac_to_rational(frac[0:i]))
    return convergents

def contfrac_to_rational (frac):
    if len(frac) == 0:
        return (0,1)
    num = frac[-1]
    denom = 1
    for i in range(-2,-len(frac)-1,-1):
        num, denom = frac[i]*num+denom, num
    return (num,denom)
####################################### End Continued Fractions ###############################

# iterative implementations
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def xgcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a; m, n = x - u * q, y - v * q
        b,a,x,y,u,v = a,r,u,v,m,n
    return b, x, y

def factorial(n):
    f = n
    for i in range(n):
        if 0 <= i <= 1:
            f *= 1
        else:
            f *= i
    return f

# recursive implementations
def r_gcd(a,b):
    if b == 0:
        return a
    else:
        return r_gcd(b, a % b)

def r_xgcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = r_xgcd(b % a, a)
        return (g, x - (b // a) * y, y)


def r_factorial(n):
    if 0 <= n <= 1:
        return 1
    else:
        return n * r_factorial(n - 1)

if __name__ == '__main__':
    print get_sqrt(25)
