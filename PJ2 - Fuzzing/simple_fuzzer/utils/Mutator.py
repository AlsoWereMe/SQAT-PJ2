import math
import random
import struct
from typing import Any


def insert_random_character(s: str) -> str:
    """
    向 s 中下标为 pos 的位置插入一个随机 byte
    pos 为随机生成，范围为 [0, len(s)]
    插入的 byte 为随机生成，范围为 [32, 127]
    """
    # TODO
    pos = random.randint(0, len(s))
    random_char = chr(random.randint(32, 127))
    return s[:pos] + random_char + s[pos:]


def flip_random_bits(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 bitflip 与 random havoc 实现相邻 N 位翻转（N = 1, 2, 4），其中 N 为随机生成
    从 s 中随机挑选一个 bit，将其与其后面 N - 1 位翻转（翻转即 0 -> 1; 1 -> 0）
    注意：不要越界
    """
    # TODO
    if not s:
        return s
    
    # 将字符串转换为字节数组
    bytes_arr = bytearray(s.encode())
    
    # 随机选择翻转位数 (1, 2, or 4)
    n_bits = random.choice([1, 2, 4])
    
    # 随机选择起始位置
    max_pos = len(bytes_arr) * 8 - n_bits
    if max_pos < 0:
        return s
    
    start_bit = random.randint(0, max_pos)
    byte_index = start_bit // 8
    bit_offset = start_bit % 8
    
    # 翻转连续的N位
    for i in range(n_bits):
        if byte_index >= len(bytes_arr):
            break
        # 创建掩码并翻转指定位
        mask = 1 << (7 - ((bit_offset + i) % 8))
        bytes_arr[byte_index] ^= mask
        if (bit_offset + i + 1) % 8 == 0:
            byte_index += 1
            
    return bytes_arr.decode(errors='ignore')


def arithmetic_random_bytes(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 arithmetic inc/dec 与 random havoc 实现相邻 N 字节随机增减（N = 1, 2, 4），其中 N 为随机生成
    字节随机增减：
        1. 取其中一个 byte，将其转换为数字 num1；
        2. 将 num1 加上一个 [-35, 35] 的随机数，得到 num2；
        3. 用 num2 所表示的 byte 替换该 byte
    从 s 中随机挑选一个 byte，将其与其后面 N - 1 个 bytes 进行字节随机增减
    注意：不要越界；如果出现单个字节在添加随机数之后，可以通过取模操作使该字节落在 [0, 255] 之间
    """
    
    # TODO
    if not s:
        return s
    
    bytes_arr = bytearray(s.encode())
    if not bytes_arr:
        return s
        
    # 随机选择操作字节数
    n_bytes = random.choice([1, 2, 4])
    if n_bytes > len(bytes_arr):
        n_bytes = len(bytes_arr)
        
    # 随机选择起始位置
    start_pos = random.randint(0, len(bytes_arr) - n_bytes)
    
    # 对连续N个字节进行变异
    for i in range(n_bytes):
        delta = random.randint(-35, 35)
        bytes_arr[start_pos + i] = (bytes_arr[start_pos + i] + delta) % 256
        
    return bytes_arr.decode(errors='ignore')


def interesting_random_bytes(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 interesting values 与 random havoc 实现相邻 N 字节随机替换为 interesting_value（N = 1, 2, 4），其中 N 为随机生成
    interesting_value 替换：
        1. 构建分别针对于 1, 2, 4 bytes 的 interesting_value 数组；
        2. 随机挑选 s 中相邻连续的 1, 2, 4 bytes，将其替换为相应 interesting_value 数组中的随机元素；
    注意：不要越界
    """
    # TODO
    if not s:
        return s
        
    # 定义有趣的值
    interesting_8 = [0x00, 0xFF, 0x7F, 0x80]
    interesting_16 = [0x0000, 0xFFFF, 0x7FFF, 0x8000]
    interesting_32 = [0x00000000, 0xFFFFFFFF, 0x7FFFFFFF, 0x80000000]
    
    bytes_arr = bytearray(s.encode())
    if not bytes_arr:
        return s
        
    # 随机选择替换字节数
    n_bytes = random.choice([1, 2, 4])
    if n_bytes > len(bytes_arr):
        n_bytes = len(bytes_arr)
        
    start_pos = random.randint(0, len(bytes_arr) - n_bytes)


def havoc_random_insert(s: str):
    """
    基于 AFL 变异算法策略中的 random havoc 实现随机插入
    随机选取一个位置，插入一段的内容，其中 75% 的概率是插入原文中的任意一段随机长度的内容，25% 的概率是插入一段随机长度的 bytes
    """
    # TODO
    if not s:
        return s
        
    bytes_arr = bytearray(s.encode())
    insert_pos = random.randint(0, len(bytes_arr))
    
    # 75%概率插入原文内容，25%概率插入随机内容
    if random.random() < 0.75 and len(bytes_arr) > 0:
        # 从原文随机选择一段
        length = random.randint(1, min(8, len(bytes_arr)))
        start = random.randint(0, len(bytes_arr) - length)
        content = bytes_arr[start:start + length]
    else:
        # 生成随机内容
        length = random.randint(1, 8)
        content = bytearray(random.randint(0, 255) for _ in range(length))
    
    bytes_arr[insert_pos:insert_pos] = content
    return bytes_arr.decode(errors='ignore')


def havoc_random_replace(s: str):
    """
    基于 AFL 变异算法策略中的 random havoc 实现随机替换
    随机选取一个位置，替换随后一段随机长度的内容，其中 75% 的概率是替换为原文中的任意一段随机长度的内容，25% 的概率是替换为一段随机长度的 bytes
    """
    # TODO
    if not s:
        return s
        
    bytes_arr = bytearray(s.encode())
    if len(bytes_arr) < 2:
        return s
        
    # 选择替换位置和长度
    replace_pos = random.randint(0, len(bytes_arr) - 1)
    max_length = min(8, len(bytes_arr) - replace_pos)
    replace_length = random.randint(1, max_length)
    
    # 75%概率使用原文内容替换，25%概率使用随机内容
    if random.random() < 0.75 and len(bytes_arr) > replace_length:
        # 从原文随机选择一段
        start = random.randint(0, len(bytes_arr) - replace_length)
        content = bytes_arr[start:start + replace_length]
    else:
        # 生成随机内容
        content = bytearray(random.randint(0, 255) for _ in range(replace_length))
    
    bytes_arr[replace_pos:replace_pos + replace_length] = content
    return bytes_arr.decode(errors='ignore')


class Mutator:

    def __init__(self) -> None:
        """Constructor"""
        self.mutators = [
            insert_random_character,
            flip_random_bits,
            arithmetic_random_bytes,
            interesting_random_bytes,
            havoc_random_insert,
            havoc_random_replace
        ]

    def mutate(self, inp: Any) -> Any:
        mutator = random.choice(self.mutators)
        return mutator(inp)
