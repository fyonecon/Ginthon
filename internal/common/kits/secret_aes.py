# -*- coding: utf-8 -*-

import base64
from Crypto.Cipher import AES # pip3 install pycryptodome
from Crypto.Util.Padding import pad, unpad

# string 转 bytes
def str_to_bytes(txt: str):
    return txt.encode("utf-8")

# 截取固定长度的字符串，从第1位
def truncate_string(text, length):
    if len(text) <= length:
        return text
    return text[:length]

# 生成指定长度范围内的随机字母数字字符串
# import random
# import string
# def rand_range_string(min_length, max_length):
#     length = random.randint(min_length, max_length)
#     characters = string.ascii_letters + string.digits
#     return "".join(random.choice(characters) for _ in range(length))

#
# _KEY = rand_range_string(16, 16)
# _IV = rand_range_string(16, 16)

# 固定密钥和IV
# KEY = str_to_bytes(truncate_string(_KEY, 16)) # 16字节 for AES-128
# IV = str_to_bytes(truncate_string(_IV, 16)) # 16字节 for AES-128

# KEY = str_to_bytes(truncate_string("edcvfrtgb1230987edcvfrtgb1230987edcvfrtgb1230987", 16)) # 16字节 for AES-128
IV = str_to_bytes(truncate_string("qazxsw#edcvfrtgb1230987@jhsallmi86421n", 16)) # 16字节 for AES-128

# 加密
def aes_encrypt(plaintext, KEY:bytes):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    padded_data = pad(plaintext.encode("utf-8"), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    # 转换为URL安全的Base64
    base64_str = base64.b64encode(encrypted_data).decode("utf-8")
    url_safe = base64_str.replace("+", "-").replace("/", "_").rstrip("=")
    return url_safe

# 解密
def aes_decrypt(encrypted_url_safe, KEY:bytes):
    # 恢复为标准Base64格式
    base64_str = encrypted_url_safe.replace("-", "+").replace("_", "/")
    padding = 4 - (len(base64_str) % 4)
    if padding != 4:
        base64_str += "=" * padding

    encrypted_data = base64.b64decode(base64_str)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_padded = cipher.decrypt(encrypted_data)
    decrypted_data = unpad(decrypted_padded, AES.block_size)
    return decrypted_data.decode("utf-8")

# test
# _txt = "djosdhoaisdfho0jdf90eu8nfoewu90834r5jfk#@kdsdkosdm#@dhsd#@121313"
# en_txt = aes_encrypt(_txt, KEY)
# de_txt = aes_decrypt(en_txt, KEY)
# print("test=", [_txt, en_txt, de_txt, KEY])