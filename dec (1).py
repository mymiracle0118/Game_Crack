import sys
import zlib
import os
import struct
import xxtea
import binascii

from os import walk
file = 'waitnet.lua'

XORkey = bytearray([0x1C, 0xA3, 0x4B, 0x13, 0x77, 0x84, 0xAA, 0x3B, 0x2B, 0xB2, 0x23, 0x7B, 0xEE, 0xEF, 0xF2, 0xA0, 0x3B, 0x2B, 0xCC])
headerz = ["DHGAMES","DHZAMES"]


xxteakey = "cxxwp5tcPIJ0x90r"

def zlibdecompress(data):
    decomp = zlib.decompress(data)
    return decomp

def zlibcompress(data):
    compress = zlib.compress(data)
    return compress

def remove_header(data,header):
    return remove_bytes(data,0,len(header))

def remove_bytes(buffer, start, end):
    fmt = '%ds %dx %ds' % (start, end-start, len(buffer)-end)  # 3 way split
    return b''.join(struct.unpack(fmt, buffer))

def XOR(data, xorkey):
    xorData = bytearray()
    x = 0
    for datab in data:
        if x < len(xorkey):
            xVal = datab ^ xorkey[x]
            xorData += xVal.to_bytes(1, 'little')
            x = x + 1
            if x==19:
                x=8
    return  xorData

def XORxxteaKey(xxteaKey):
    _new_key = bytearray(16)

    for indexKey in range(len(xxteaKey)):
        keyByte = ord(xxteaKey[indexKey])
        if ((keyByte - 48) & 0xff) > 9:
            if ((keyByte - 97)& 0xff) > 25:
                if ((keyByte - 65)& 0xff) <= 25:
                    keyByte = (keyByte - 62) % 26 + 65
            else:
                keyByte = (keyByte - 83) % 26 + 97
        else:
            keyByte = (keyByte - 45) % 10 + 48
        _new_key[indexKey] = keyByte
    v16 = _new_key[12]
    v17 = _new_key[5] ^ v16
    v18 = v16 ^ v17
    _new_key[12] = v18
    _new_key[5] = v17 ^ v18
    v19 = _new_key[6]
    v20 = _new_key[1] ^ v19
    v21 = v19 ^ v20
    _new_key[6] = v21
    _new_key[1] = v20 ^ v21
    v22 = _new_key[7]
    v23 = _new_key[15] ^ v22
    v24 = v22 ^ v23
    _new_key[7] = v24
    _new_key[15] = v23 ^ v24
    return  _new_key


def finish_encryption(realfile):
    clean_data = open(realfile, 'rb').read()
    zlib_data = zlibcompress(clean_data)
    xor_key = XORxxteaKey(xxteakey)
    new_data = bytearray(headerz[1], 'utf8') + zlib_data
    new_data = xxtea.encrypt(bytes(new_data), bytes(xor_key))
    xor_data = XOR(new_data, XORkey)
    new_data = bytearray(headerz[0], 'utf8') + xor_data
    realfile = realfile.replace('[d]','')
    open(realfile, 'wb').write(new_data)

def finish_decryption(realfile,file):
    tmpData = open(realfile, 'rb').read()
    if any(bytes(header, 'utf8') in tmpData for header in headerz):
        data = remove_header(open(realfile, 'rb').read(), headerz[0])
        xor_data = XOR(data, XORkey)
        xor_key = XORxxteaKey(xxteakey)
        new_data = remove_header(xxtea.decrypt(bytes(xor_data), bytes(xor_key)), headerz[1])
        final_data = zlibdecompress(new_data)
        open(realfile.replace(file,'[d]'+file), 'wb').write(final_data)

def decrypt_files(file = ''):
    if len(file)>0:
        realfile = file
        if os.path.exists(realfile):finish_decryption(realfile)
    else: #decrypt all
        for dir, subdir, files in os.walk('assets/'):
            for file in files:
                realfile = os.path.join(dir, file)
                if (not '[d]' in realfile): finish_decryption(realfile,file)

def encrypt_files(file = ''):
    if len(file)>0:
        realfile = file
        if os.path.exists(realfile):finish_encryption(realfile)
    else: #encrypt all
        for dir, subdir, files in os.walk('modassets/'):
            for file in files:
                realfile = os.path.join(dir, file)
                if ('[d]' in realfile): finish_encryption(realfile)


#encrypt_files()
decrypt_files()
