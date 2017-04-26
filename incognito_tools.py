import rsaxploit.rsa as rsa
import baseconverter.baseconverter as bc
import argparse
import sys

def converter(args):
    option = args.c2
    value = args.type
    if option == 'b64':
        print bc.b64decoder(value)
    elif option == 'h2i':
        print bc.hex2int(value)
    elif option == 'h2a':
        print bc.hex2ascii(value)
    elif option == 'a2h':
        print bc.ascii2hex(value)
    elif option == 'b2a':
        print bc.binary2ascii(value)
    elif option == 'a2b':
        print bc.ascii2binary(value)
    elif option =='i2h':
        print bc.int2hex(value)

def rsa_xploit(args):
    verbose = args.verbose
    option = args.type
    if verbose:
        rsa.VERBOSE = True

    if option == 'lowN':
        if args.N and args.p and args.q and args.e and args.c:
            d = rsa.low_n_attack(args.N, args.e, args.p, args.q)
            print rsa.decrypt(args.c, d, args.N)
        elif args.N and args.e and args.c:
            d = rsa.low_n_attack(args.N, args.e)
            print rsa.decrypt(args.c, d, args.N)
        elif args.p and args.q and args.e and args.c:
            N = args.p * args.q
            d = rsa.low_n_attack(N, args.e, args.p, args.q)
            print decrypt(args.c, d, N)
    elif option == 'wieners':
        if args.N and args.e and args.c:
            d = rsa.wieners_attack(args.e, args.N)
            print rsa.decrypt(args.c, d, args.N)
    elif option == 'PEM':
        if args.N and args.e:
            print rsa.getPemRepresentation(args.N, args.e)
    elif option == 'DER':
        if args.N and args.e:
            print rsa.getDerRepresentation(args.N, args.e)

if __name__ == '__main__':

    prog = sys.argv[1] if sys.argv[1] else '-help'
    parser = argparse.ArgumentParser()

    if prog == '-convert':
        parser.add_argument('-convert', dest='c2' ,help='Base Converter', choices=['b64', 'h2a', 'a2h', 'b2a', 'a2b', 'h2i', 'i2h'])
        parser.add_argument('type', type=str, help='String you want to convert')
        parser.add_argument('-s', type=str, help='As string (use on b64 option only)')
        converter(parser.parse_args())
    elif prog == '-rsa':
        parser.add_argument('-rsa', dest='type', help='Xploit RSA', choices=['lowN', 'wieners', 'PEM', 'DER'])
        parser.add_argument('-n', dest='N', type=int, help='RSA Modulus')
        parser.add_argument('-p', dest='p', type=int, help='RSA Coprime p')
        parser.add_argument('-q', dest='q', type=int, help='RSA Coprime q')
        parser.add_argument('-e', dest='e', type=int, help='RSA public exponent')
        parser.add_argument('-d', dest='d', type=int, help='RSA private exponent')
        parser.add_argument('-c', dest='c', type=int, help='RSA ciphertext')
        parser.add_argument('-v', dest='verbose', help='Gives more information' ,action='store_const', const=True)
        rsa_xploit(parser.parse_args())
