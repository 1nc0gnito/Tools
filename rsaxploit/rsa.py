import custommath.custommath as cm

def wieners_attack(e, N):
    frac = cm.rational_to_contfrac(e, N)
    convergents = cm.convergents_from_contfrac(frac)
    for k, d in convergents:
        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            s = n - phi + 1
            discr = s*s - 4 * n
            if discr >= 0:
                t = cm.is_perfect_sqr(discr)
                if t != -1 and (s + t) % 2 == 0:
                    print "Wiener Exploited"
                    return d
    print "Shit"
    return None

def low_n_attack(p, q, e):
    if p != q:
        phi = (p - 1) * (q - 1)
    else:
        phi = (p**2) - p
    return cm.mod_inv(e, phi)

def decrypt(c, d, n):
    m = hex(pow(c,d,n))[2:-1]
    return m.decode('hex')
