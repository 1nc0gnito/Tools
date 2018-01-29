import base64

__BYTE = 32 # amount of bytes that can be represented in binary change if needed to convert numbers bigger than 2^32

def padbinary(binarystring):
    """
        Pads with leading zeros if binary string ('00001111')
        lenght is not a multiple of 8
    """
    if len(binarystring) % __BYTE:
        while len(binarystring) % __BYTE:
            binarystring = '0' + binarystring
    return binarystring

def binaryserialize(binarystring):
    """
        Takes a binary string and outputs a list
        of bytes ex 1010101010101010 => [10101010, 10101010]
    """
    bytelist = []
    bstr = ''
    padded = padbinary(binarystring)
    for i in range(len(padded)):
        bstr += padded[i]
        if (i + 1) % __BYTE == 0:
            bytelist.append(bstr)
            bstr = ''
    return bytelist

def binary2ascii(binarystring):
    """
        Converts binarystring to ascii
        ex. '01100001' => 'a'
    """
    bytelist = binaryserialize(binarystring)
    return ''.join(chr(int(byte, 2)) for byte in bytelist)

def ascii2int_list(asciistring):
    """
        Convert an ascii string to an int (dec ascii representation)
        list
        ex. 'abcd' => [97, 98, 99, 100]
    """
    return [ord(ch) for ch in asciistring]

def ascii2int(asciistring):
    """
        Converts an ascii string into an int string
        ex. 'abcd' => '979899100'
    """
    return ''.join(str(ord(ch)) for ch in asciistring)

def ascii2binary(asciistring):
    """
        Converts a ascii string to a binary string
        ex. 'ab' => 0110000101100010
    """
    ordlist = ascii2int_list(asciistring)
    return ''.join(int2binary(o) for o in ordlist)

def int2binary(ascii_n_rep):
    """
        Convert a number 'n' to binary string
        ex. '97' => '01100001'
    """
    byte = ''
    for i in range(__BYTE):
        if int(ascii_n_rep) & (1 << i):
            byte += '1'
        else:
            byte += '0'
    return byte[::-1]

def binary2int(binarystring, padded=True):
    """
        Converts a binary string into a string of int
        ex. 0110000101100010 => '97 98'
        if padded = False then '9798'
    """
    bytelist = binaryserialize(binarystring)
    return ' '.join(str(int(byte, 2)) for byte in bytelist) \
           if padded \
           else ''.join(str(int(byte, 2)) for byte in bytelist)

def ascii2hex(asciistring):
    """
        Converts an ascii string into hex string
        ex. 'ab' => '6566'
    """
    return asciistring.encode('hex')

def hex2ascii(hexstring):
    """
        Converts a hex string to ascii
        ex. '6566' => 'ab'
    """
    return hexstring.decode('hex')

def hex2int(hexstring):
    """
        Converts a hex string into integer
        ex. 65 => 97
    """
    if '0x' in hexstring:
        hstr = hexstring.replace('0x', '')
    return int(hexstring, 16)

def int2hex(integer):
    """
        Converts an integer string into hex string
        ex. 97 => 65
    """
    return hex(int(integer))[2:]

def __openfile(file):
    """
        Opens a file and return its content
        file is the filename of the file
    """
    f = open(file, 'r')
    content = f.read()
    f.close()
    return content

def b64decoder(b64EncFile, isFile=True):
    """
        Decodes a base64 string recursively by default
    """
    b64str = __openfile(b64EncFile) if isFile else b64EncFile
    while True:
        try:
            b64str = base64.b64decode(b64str)
            print b64str
        except:
            break
    return b64str
