class RC4:
    def __init__(self):
        self.S = []
    
    def set_key(self, K: bytes, keylen: int):
        """ 初始化S盒 """
        self.S = list(range(256))
        j = 0
        for i in range(256):
            # 确保K的索引有效，i % keylen 不会超出K的范围
            j = (j + self.S[i] + K[i % keylen]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
    
    def transform(self, data: bytes) -> bytes:
        """ 加密或解密数据 """
        i = 0
        j = 0
        output = bytearray()
        S = self.S.copy()  # 使用副本来保持原始S盒状态不变
        
        for k in range(len(data)):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            key = S[(S[i] + S[j]) % 256]
            output.append(key ^ data[k])
        
        return bytes(output)

if __name__ == "__main__":
    data = b"wednesday is shit"
    print("明文:", data.decode())
    
    # 注意：C++版本密钥包含结尾的null，这里显式添加\x00
    K = 'key'.encode()
    keylen = len(K)  # 12字节（包含null）
    
    rc4_encrypt = RC4()
    rc4_decrypt = RC4()
    
    rc4_encrypt.set_key(K, keylen)
    rc4_decrypt.set_key(K, keylen)
    
    # 加密
    encrypted = rc4_encrypt.transform(data)

    print("密文:", encrypted.hex())  # 使用hex显示二进制更清晰
    
    # 解密
    decrypted = rc4_decrypt.transform(encrypted)
    print("解密后明文:", decrypted.decode())