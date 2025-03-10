import math


def md5(message):

    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    def left_rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    F = lambda x, y, z: (x & y) | (~x & z)
    G = lambda x, y, z: (x & z) | (y & ~z)
    H = lambda x, y, z: x ^ y ^ z
    I = lambda x, y, z: y ^ (x | ~z)

    T = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
    s = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4

    orig_len = len(message)
    message = bytearray(message)
    bit_len = orig_len * 8
    
    message.append(0x80)
    while (len(message) * 8) % 512 != 448:
        message.append(0x00)
    
    message += bit_len.to_bytes(8, 'little')


    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset+64]
        M = [int.from_bytes(chunk[j:j+4], 'little') for j in range(0, 64, 4)]
        
        a, b, c, d = A, B, C, D
        
        for i in range(64):
            if 0 <= i < 16:
                f = F(b, c, d)
                g = i
            elif 16 <= i < 32:
                f = G(b, c, d)
                g = (5*i + 1) % 16
            elif 32 <= i < 48:
                f = H(b, c, d)
                g = (3*i + 5) % 16
            else:
                f = I(b, c, d)
                g = (7*i) % 16
            
            f = (f + a + T[i] + M[g]) & 0xFFFFFFFF
            a = d
            d = c
            c = b
            b = (b + left_rotate(f, s[i])) & 0xFFFFFFFF
        
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    return f"{A.to_bytes(4, 'little').hex()}{B.to_bytes(4, 'little').hex()}" \
           f"{C.to_bytes(4, 'little').hex()}{D.to_bytes(4, 'little').hex()}"

message = "123".encode('utf-8')
print("MD5加密结果:", md5(message))

import hashlib
print('加解密结果是否一致',md5(message) == hashlib.md5(message).hexdigest())


