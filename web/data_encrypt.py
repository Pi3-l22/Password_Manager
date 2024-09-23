import hashlib
import secrets
import string
import json

from Cryptodome.Cipher import AES, ChaCha20
from Cryptodome.Random import get_random_bytes
from pysm4 import encrypt_ecb, decrypt_ecb

# 状态码
OK = 1
ERROR = -1


# 所有加密算法均使用SHA-256哈希算法PBKDF2迭代1000次生成密钥
# 主密钥使用SHA3-256哈希算法进行加密


# SHA3-256
def sha3_256(data):
    return hashlib.sha3_256(data.encode()).hexdigest()


# PBKDF2
# 使用sha256/sm3作为hash算法，盐值固定生成，迭代10000次，生成256位密钥
def pbkdf2(data):
    salt = b'Pi3@l22_hdu&'
    return hashlib.pbkdf2_hmac('sha256', data.encode(), salt, 10000).hex()


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


# SM4 加密
def sm4_encrypt(data, key):
    """
    :param data: --> 字符串
    :param key: --> 十六进制字符串
    :return: --> 十六进制字符串
    """
    # key不能超过16字节 超过截断
    if len(key) > 16:
        key = key[:16]
    return encrypt_ecb(data, key)


# SM4 解密
def sm4_decrypt(data, key):
    """
    :param data: --> 十六进制字符串
    :param key: --> 十六进制字符串
    :return: --> 字符串
    """
    # key不能超过16字节 超过截断
    if len(key) > 16:
        key = key[:16]
    return decrypt_ecb(data, key)


# 随机生成强密码字符串
def random_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation.replace(",", "").replace(":", "")
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


# 数据加密接口
def data_encrypt(data, key, algorithm):
    if algorithm == 'AES-256':
        return aes_encrypt(data, key)
    elif algorithm == 'ChaCha20':
        return chacha20_encrypt(data, key)
    elif algorithm == 'XChaCha20':
        return xchacha20_encrypt(data, key)
    elif algorithm == 'SM4-ECB':
        return sm4_encrypt(data, key)
    else:
        return None


# 数据解密接口 
def data_decrypt(data, key, algorithm):
    if algorithm == 'AES-256':
        return aes_decrypt(data, key)
    elif algorithm == 'ChaCha20':
        return chacha20_decrypt(data, key)
    elif algorithm == 'XChaCha20':
        return xchacha20_decrypt(data, key)
    elif algorithm == 'SM4-ECB':
        return sm4_decrypt(data, key)
    else:
        return None


# 获取密码信息数据导出成json格式数据
def export_password_to_json(data: list, username, key, dir_path):
    # key = sha_256(key)
    key = pbkdf2(key)
    pwd_info_list = []
    try:
        for item in data:
            pwd_info_list.append(
                {
                    'username': item['username'],
                    'website_name': item['website_name'],
                    'website': item['website'],
                    'account': item['account'],
                    'password': data_decrypt(item['password_encrypted'], key, item['encrypted_method']),
                    'encrypted_method': item['encrypted_method'],
                    'note': item['note'],
                    'created_at': item['created_at']
                }
            )
        json_data = json.dumps(pwd_info_list, ensure_ascii=False, indent=4)
        with open(f"{dir_path}\\{username}_passwords.json", 'w') as f:
            f.write(json_data)
        return OK
    except Exception as e:
        return ERROR


# 获取密码信息数据导出成CSV格式数据
def export_password_to_csv(data: list, username, key, dir_path):
    # key = sha_256(key)
    key = pbkdf2(key)
    try:
        with open(f"{dir_path}\\{username}_passwords.csv", 'w', encoding='UTF-8') as f:
            f.write('username,website_name,website,account,password,encrypted_method,note,created_at\n')
            for item in data:
                f.write(
                    f"{item['username']},{item['website_name']},{item['website']},{item['account']},"
                    f"{data_decrypt(item['password_encrypted'], key, item['encrypted_method'])},{item['encrypted_method']},"
                    f"{item['note']},{item['created_at']}\n"
                )
        return OK
    except Exception as e:
        return ERROR


# 获取密码信息数据导出成TXT格式数据
def export_password_to_txt(data: list, username, key, dir_path):
    # key = sha_256(key)
    key = pbkdf2(key)
    count = 1
    try:
        with open(f"{dir_path}\\{username}_passwords.txt", 'w', encoding='UTF-8') as f:
            for item in data:
                f.write(
                    f"---------------{count}---------------\n"
                    f"username: {item['username']}\n"
                    f"website_name: {item['website_name']}\n"
                    f"website: {item['website']}\n"
                    f"account: {item['account']}\n"
                    f"password: {data_decrypt(item['password_encrypted'], key, item['encrypted_method'])}\n"
                    f"encrypted_method: {item['encrypted_method']}\n"
                    f"note: {item['note']}\n"
                    f"created_at: {item['created_at']}\n\n"
                )
                count += 1
        return OK
    except Exception as e:
        return ERROR


# 导出数据接口
def export_password(data: list, username, key, dir_path, export_format):
    if export_format == 'JSON':
        return export_password_to_json(data, username, key, dir_path)
    elif export_format == 'CSV':
        return export_password_to_csv(data, username, key, dir_path)
    elif export_format == 'TXT':
        return export_password_to_txt(data, username, key, dir_path)
    else:
        return ERROR


# 导入JSON格式数据
def import_password_from_json(username, file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            pwd_info_list = []
            for item in data:
                if username != item['username']:
                    continue
                pwd_info_list.append(
                    {
                        'username': item['username'],
                        'website_name': item['website_name'],
                        'website': item['website'],
                        'account': item['account'],
                        'password': item['password'],
                        'encrypted_method': item['encrypted_method'],
                        'note': item['note'],
                        # 'created_at': item['created_at']
                    }
                )
            return pwd_info_list
    except Exception as e:
        return ERROR


# 导入CSV格式数据
def import_password_from_csv(username, file_path):
    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            data = f.readlines()
            pwd_info_list = []
            for item in data[1:]:
                item = item.strip().split(',')
                if username != item[0]:
                    continue
                pwd_info_list.append(
                    {
                        'username': item[0],
                        'website_name': item[1],
                        'website': item[2],
                        'account': item[3],
                        'password': item[4],
                        'encrypted_method': item[5],
                        'note': item[6],
                        # 'created_at': item[7]
                    }
                )
            return pwd_info_list
    except Exception as e:
        return ERROR


# 导入TXT格式数据
def import_password_from_txt(username, file_path):
    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            data = f.readlines()
            pwd_info_list = []
            count = 1
            for i in range(len(data)):
                if data[i].startswith('---------------'):
                    item = {
                        'username': data[i + 1].split(': ')[1].strip(),
                        'website_name': data[i + 2].split(': ')[1].strip(),
                        'website': data[i + 3].split(': ')[1].strip(),
                        'account': data[i + 4].split(': ')[1].strip(),
                        'password': data[i + 5].split(': ')[1].strip(),
                        'encrypted_method': data[i + 6].split(': ')[1].strip(),
                        'note': data[i + 7].split(': ')[1].strip(),
                        # 'created_at': data[i + 8].split(': ')[1].strip()
                    }
                    if username != item['username']:
                        continue
                    pwd_info_list.append(item)
                    count += 1
            return pwd_info_list
    except Exception as e:
        return ERROR


# 导入数据接口
def import_password(username, file_path, import_format):
    if import_format == 'JSON':
        return import_password_from_json(username, file_path)
    elif import_format == 'CSV':
        return import_password_from_csv(username, file_path)
    elif import_format == 'TXT':
        return import_password_from_txt(username, file_path)
    else:
        return ERROR
