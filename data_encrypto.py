import hashlib
import secrets
import string
from Cryptodome.Cipher import AES, ChaCha20
from Cryptodome.Random import get_random_bytes


# 所有加密算法均使用SHA-256哈希算法生成密钥
# 主密钥使用SHA3-256哈希算法进行加密

# SHA-256
def sha_256(data):
    return hashlib.sha256(data.encode()).hexdigest()


# SHA3-256
def sha3_256(data):
    return hashlib.sha3_256(data.encode()).hexdigest()


# AES-256 加密
def aes_encrypt(data, key):
    """
    :param data: --> 字符串
    :param key: --> 十六进制字符串
    :return: --> 十六进制字符串
    """
    # 十六进制key转换为字节
    key = bytes.fromhex(key)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    # 将tag、nouce、ciphertext合并转换为十六进制字符串
    return nonce.hex() + tag.hex() + ciphertext.hex()


# AES-256 解密
def aes_decrypt(data, key):
    """
    :param data: --> 十六进制字符串
    :param key: --> 十六进制字符串
    :return: --> 字符串
    """
    # 十六进制key转换为字节
    key = bytes.fromhex(key)
    # 将十六进制字符串转换为tag、nouce、ciphertext字节串
    nonce = bytes.fromhex(data[:32])
    tag = bytes.fromhex(data[32:64])
    ciphertext = bytes.fromhex(data[64:])
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()


# ChaCha20 加密
def chacha20_encrypt(data, key):
    """
    :param data: --> 字符串
    :param key: --> 十六进制字符串
    :return: --> 十六进制字符串
    """
    # 十六进制key转换为字节
    key = bytes.fromhex(key)
    # 生成12字节随机数
    nonce = get_random_bytes(12)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(data.encode())
    # 将nouce、ciphertext合并转换为十六进制字符串
    return nonce.hex() + ciphertext.hex()


# ChaCha20 解密
def chacha20_decrypt(data, key):
    """
    :param data: --> 十六进制字符串
    :param key: --> 十六进制字符串
    :return: --> 字符串
    """
    # 十六进制key转换为字节
    key = bytes.fromhex(key)
    # 将十六进制字符串转换为nouce、ciphertext字节串
    nonce = bytes.fromhex(data[:24])
    ciphertext = bytes.fromhex(data[24:])
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()


# Xchacha20 加密
def xchacha20_encrypt(data, key):
    """
    :param data: --> 字符串
    :param key: --> 十六进制字符串
    :return: --> 十六进制字符串
    """
    # 十六进制key转换为字节
    key = bytes.fromhex(key)
    # 生成24字节随机数
    nonce = get_random_bytes(24)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(data.encode())
    # 将nouce、ciphertext合并转换为十六进制字符串
    return nonce.hex() + ciphertext.hex()


# Xchacha20 解密
def xchacha20_decrypt(data, key):
    """
    :param data: --> 十六进制字符串
    :param key: --> 十六进制字符串
    :return: --> 字符串
    """
    # 十六进制key转换为字节
    key = bytes.fromhex(key)
    # 将十六进制字符串转换为nouce、ciphertext字节串
    nonce = bytes.fromhex(data[:48])
    ciphertext = bytes.fromhex(data[48:])
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()


# 随机生成强密码字符串
def random_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

