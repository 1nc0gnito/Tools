import custommath.custommath as cm
from pyasn1.codec.der import encoder
from pyasn1.type.univ import *
import base64
import re
import requests
import time

__PEM_TEMPLATE = '-----BEGIN RSA PRIVATE KEY-----\n%s-----END RSA PRIVATE KEY-----\n'
SILENT = False

def getprimes(n, silent=True):
    """
        --getprimes--
            will take the N modulus of RSA public key and
            connects to factordb.com to retrieve possible coprimes p and q
    """
    if not SILENT:
        print "[+] Retrieving Factors of N from www.factordb.com"
    try:
        url = 'http://factordb.com/index.php?query={}'
        id_url = 'http://factordb.com/index.php?id={}'
        req = requests.get(url.format(n))
        regex = re.compile('index\.php\?id\=([0-9]+)', re.IGNORECASE)
        n_id, p_id, q_id = regex.findall(req.text)
        p_req = requests.get(id_url.format(p_id))
        q_req = requests.get(id_url.format(q_id))
        regex = re.compile('value=\"([0-9]+)\"', re.IGNORECASE)
        p = int(regex.findall(p_req.text)[0])
        q = int(regex.findall(q_req.text)[0])
        if p == q == n:
            p = n
            q = 1
    except Exception as e:
        raise 'Connection error {}'.format(e)
    if not SILENT:
        print "\t[-] Factors Retrieved Successfuly\n\t[p] --> {}\n\t[q] --> {}".format(p, q)
    return p, q

def wieners_attack(e, N):
    """
        --wieners_attack--
            Performs the wieners attack to discover the
            private exponent d of an rsa when the public exponent e
            is too big
    """
    if SILENT:
        print '[x] Performing Wieners attack'
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
                    if SILENT:
                        print "[!!] Wiener Exploited [!!]\n\t[d] --> {}".format(d)
                    return d
    if SILENT:
        print "[o_o] Not Weiner Vulnerable!"
    return -1

def low_n_attack(n, e, p=0, q=0):
    """
        --low_n_attack--
            Exploits the low n vulnerability by
            finding the factors of n (p and q)
    """
    if SILENT:
        print "[x] Exploiting low n vulnerability"
    if not p and not q:
        p , q = getprimes(n)
    phi = (p - 1) * (q - 1)
    return cm.mod_inv(e, phi)

def decrypt(c, d, n):
    m = hex(pow(c,d,n))[2:-1]
    return m.decode('hex')

def toDer(n, e, p, q):
        seq = Sequence()
        d = cm.mod_inv(e, (p-1)*(q-1))
        dp = d % (p-1)
        dq = d % (q-1)
        qInv = cm.mod_inv(q, p)
        for x in [0, n, e, d, p, q, dp, dq, qInv]:
            seq.setComponentByPosition(len(seq), Integer(x))
        return encoder.encode(seq)

def toPEM(n, e, p, q):
        return (__PEM_TEMPLATE % base64.encodestring(toDer(n,e,p,q)).decode()).encode()

def getPemRepresentation(n, e):
    p, q = getprimes(n)
    return toPEM(n,e,p,q)

def getDerRepresentation(n, e):
    p, q = getprimes(n)
    return toDer(n,e,p,q)

if __name__ == "__main__":
    n = int(0x00aa18aba43b50deef38598faf87d2ab634e4571c130a9bca7b878267414faab8b471bd8965f5c9fc3818485eaf529c26246f3055064a8de19c8c338be5496cbaeb059dc0b358143b44a35449eb264113121a455bd7fde3fac919e94b56fb9bb4f651cdb23ead439d6cd523eb08191e75b35fd13a7419b3090f24787bd4f4e1967)
    p = 10272507984759283768184415823001782212803274857375688280678837373891542550268707041884550332766324551399377658257839771525050268735407698239431037942292507
    q = 11627708886355621199735412802139569467434585415329927587631124833895119494317513796736733307101074383089140602809318017663635247723052449998061148241098917
    e = 65537
    d = wieners_attack(e, n)
    print d
