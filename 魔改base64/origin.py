
def base64_encode(data):
    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    data_bytes = data if isinstance(data, bytes) else data.encode('utf-8')
    pad_num = (3 - (len(data_bytes) % 3)) % 3
    data_padded = data_bytes + bytes([0] * pad_num)
    encoded = []
    
    for i in range(0, len(data_padded), 3):
        chunk = data_padded[i:i+3]
        combined = (chunk[0] << 16) | (chunk[1] << 8) | chunk[2]
        indices = [
            (combined >> 18) & 0x3F,
            (combined >> 12) & 0x3F,
            (combined >> 6) & 0x3F,
            combined & 0x3F,
        ]
        encoded_chunk = ''.join([BASE64_CHARS[idx] for idx in indices])
        encoded.append(encoded_chunk)
    
    encoded_str = ''.join(encoded)
    if pad_num:
        encoded_str = encoded_str[:-pad_num] + '=' * pad_num
    return encoded_str


def base64_decode(encoded_str):
    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    encoded_str = encoded_str.rstrip('=')
    pad_num = (4 - (len(encoded_str) % 4)) % 4
    encoded_str += '=' * pad_num
    
    decoded_bytes = bytearray()
    
    for i in range(0, len(encoded_str), 4):
        chunk = encoded_str[i:i+4].ljust(4, 'A')
        indices = []
        for c in chunk:
            if c == '=':
                indices.append(0)
            else:
                index = BASE64_CHARS.find(c)
                if index == -1:
                    raise ValueError(f"Invalid character: {c}")
                indices.append(index)
        
        combined = (indices[0] << 18) | (indices[1] << 12) | (indices[2] << 6) | indices[3]
        b1 = (combined >> 16) & 0xFF
        b2 = (combined >> 8) & 0xFF
        b3 = combined & 0xFF
        decoded_bytes.extend([b1, b2, b3])
    
    pad_num = encoded_str.count('=', 0, len(encoded_str))
    if pad_num:
        decoded_bytes = decoded_bytes[:-pad_num]
    return bytes(decoded_bytes)




original_data = '疯狂的坤坤'.encode('utf-8')
encoded_str = base64_encode(original_data)
print(f"Encoded: {encoded_str}")


decoded_data = base64_decode(encoded_str)
print(f"Decoded: {decoded_data.decode('utf-8')}")