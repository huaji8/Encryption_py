#测试魔改算法雪崩效应是否达标
import math
import random
from typing import Callable
def md5(message):
    A = 0x89ABCDEF
    B = 0xFEDCBA98
    C = 0x01234567
    D = 0x76543210
    '''
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    '''

    def left_rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    F = lambda x, y, z: (x & y) | (~x & z)
    G = lambda x, y, z: (x & z) | (y & ~z)
    H = lambda x, y, z: x ^ y ^ z
    I = lambda x, y, z: y ^ (x | ~z)
    
    T = [int(abs(math.cos(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
#   T = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

    s = [5,9,14,20]*4 + [6,11,16,23]*4 + [4,10,17,22]*4 + [7,12,15,21]*4
#   s = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4

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






def generate_test_cases(num_cases: int = 1000, data_len: int = 64) -> list:
    """
    生成随机测试用例对
    :param num_cases: 测试用例数量
    :param data_len: 每个测试数据的字节长度
    :return: 包含(原始数据, 修改数据)的列表
    """
    test_cases = []
    for _ in range(num_cases):
        # 生成随机原始数据
        original = bytes([random.randint(0, 255) for _ in range(data_len)])
        
        # 随机选择要翻转的位
        flip_byte = random.randint(0, data_len-1)
        flip_bit = random.randint(0, 7)
        # 创建修改后的数据
        modified = bytearray(original)
        modified[flip_byte] ^= (1 << flip_bit)
        test_cases.append((bytes(original), bytes(modified)))
    
    return test_cases

def hex_to_bits(hex_str: str) -> list:
    """
    将十六进制哈希值转换为二进制位列表
    :param hex_str: 十六进制字符串
    :return: 二进制位列表（0/1）
    """
    bits = []
    for byte in bytes.fromhex(hex_str):
        bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
    return bits

def avalanche_test(hash_func: Callable[[bytes], str], test_cases: list) -> list:
    """
    执行雪崩效应测试
    :param hash_func: 要测试的哈希函数
    :param test_cases: 测试用例列表
    :return: 包含测试结果的字典列表
    """
    results = []
    for original, modified in test_cases:
        # 计算哈希值
        hash_orig = hash_func(original)
        hash_mod = hash_func(modified)
        
        # 转换为二进制位
        bits_orig = hex_to_bits(hash_orig)
        bits_mod = hex_to_bits(hash_mod)
        
        # 计算变化位数
        changed_bits = sum(b1 != b2 for b1, b2 in zip(bits_orig, bits_mod))
        total_bits = len(bits_orig)
        
        results.append({
            'original': original.hex(),
            'modified': modified.hex(),
            'hash_orig': hash_orig,
            'hash_mod': hash_mod,
            'changed_bits': changed_bits,
            'changed_percent': changed_bits / total_bits * 100
        })
    
    return results

def analyze_results(results: list) -> dict:
    """
    分析测试结果
    :param results: 测试结果列表
    :return: 包含统计信息的字典
    """
    total_tests = len(results)
    total_bits = len(hex_to_bits(results[0]['hash_orig']))
    
    # 基础统计
    changed_bits = [r['changed_bits'] for r in results]
    avg_changed = sum(changed_bits) / total_tests
    min_changed = min(changed_bits)
    max_changed = max(changed_bits)
    
    # 分布统计
    distribution = {}
    for bits in changed_bits:
        distribution[bits] = distribution.get(bits, 0) + 1
    
    return {
        'total_tests': total_tests,
        'total_bits': total_bits,
        'avg_changed': avg_changed,
        'min_changed': min_changed,
        'max_changed': max_changed,
        'distribution': distribution
    }

def print_report(stats: dict):
    print(f"=== 雪崩效应测试报告 ===")
    print(f"总测试次数: {stats['total_tests']}")
    print(f"哈希值长度: {stats['total_bits']} bits")
    print(f"\n变化位数统计:")
    print(f"平均变化位数: {stats['avg_changed']:.2f} ({stats['avg_changed']/stats['total_bits']*100:.2f}%)")
    print(f"最小变化位数: {stats['min_changed']}")
    print(f"最大变化位数: {stats['max_changed']}")
    
    print("\n分布情况 (前10位):")
    sorted_dist = sorted(stats['distribution'].items(), key=lambda x: x[1], reverse=True)[:10]
    for bits, count in sorted_dist:
        print(f"{bits:3d} bits: {count:4d} 次 | {'■' * (count // (stats['total_tests'] // 50))}")



if __name__ == "__main__":


    def test_hash(data: bytes) -> str:
        return md5(data)

    # 生成测试数据
    test_cases = generate_test_cases(num_cases=1000)
    results = avalanche_test(test_hash, test_cases)
    stats = analyze_results(results)
    print_report(stats)


    # 验证雪崩效应
    ideal = stats['total_bits'] / 2
    print('雪崩效应是否达标',abs(stats['avg_changed'] - ideal) < ideal * 0.1)