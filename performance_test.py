import data_encrypt as de
import database_op as db
import time

# 各部分性能测试

# 数据加密性能测试
# SHA3-256
time_start = time.time()
hash_sha3 = de.sha3_256('123456')
time_end = time.time()
print(f'SHA3-256 time: {time_end - time_start}')

# PBKDF2
time_start = time.time()
hash_pbkdf2 = de.pbkdf2('123456')
time_end = time.time()
print(f'PBKDF2 time: {time_end - time_start}')

# AES-256
time_start = time.time()
aes_encrypted = de.data_encrypt('123456', de.pbkdf2('123456'), 'AES-256')
time_end = time.time()
print(f'AES-256 encrypto time: {time_end - time_start}')
time_start = time.time()
aes_decrypted = de.data_decrypt(aes_encrypted, de.pbkdf2('123456'), 'AES-256')
time_end = time.time()
print(f'AES-256 decrypto time: {time_end - time_start}')

# ChaCha20
time_start = time.time()
chacha20_encrypted = de.data_encrypt('123456', de.pbkdf2('123456'), 'ChaCha20')
time_end = time.time()
print(f'ChaCha20 encrypto time: {time_end - time_start}')
time_start = time.time()
chacha20_decrypted = de.data_decrypt(chacha20_encrypted, de.pbkdf2('123456'), 'ChaCha20')
time_end = time.time()
print(f'ChaCha20 decrypto time: {time_end - time_start}')

# XChaCha20
time_start = time.time()
xchacha20_encrypted = de.data_encrypt('123456', de.pbkdf2('123456'), 'XChaCha20')
time_end = time.time()
print(f'XChaCha20 encrypto time: {time_end - time_start}')
time_start = time.time()
xchacha20_decrypted = de.data_decrypt(xchacha20_encrypted, de.pbkdf2('123456'), 'XChaCha20')
time_end = time.time()
print(f'XChaCha20 decrypto time: {time_end - time_start}')

# SM4-ECB
time_start = time.time()
sm4_encrypted = de.data_encrypt('123456', de.pbkdf2('123456'), 'SM4-ECB')
time_end = time.time()
print(f'SM4-ECB encrypto time: {time_end - time_start}')
time_start = time.time()
sm4_decrypted = de.data_decrypt(sm4_encrypted, de.pbkdf2('123456'), 'SM4-ECB')
time_end = time.time()
print(f'SM4-ECB decrypto time: {time_end - time_start}')

# 随机生成强密码
time_start = time.time()
strong_password = de.random_password(16)
time_end = time.time()
print(f'Strong password generation time: {time_end - time_start}')

# 数据库操作性能测试
# 查询用户表
time_start = time.time()
db.query_user(db.conn, 'admin')
time_end = time.time()
print(f'Query user time: {time_end - time_start}')

# 插入用户表
time_start = time.time()
db.insert_user(db.conn, 'test1', 'test1')
time_end = time.time()
print(f'Insert user time: {time_end - time_start}')

# 查询密码表
time_start = time.time()
db.query_password(db.conn, 'admin')
time_end = time.time()
print(f'Query password time: {time_end - time_start}')

# 插入密码表
time_start = time.time()
db.insert_password(db.conn, 'test1', 'test1', 'test1', 'test1', 'test1', 'test1', 'test1')
time_end = time.time()
print(f'Insert password time: {time_end - time_start}')

# 查询密码创建时间
time_start = time.time()
db.query_password_created_at(db.conn, 'test1', 'test1', 'test1')
time_end = time.time()
print(f'Query password created time: {time_end - time_start}')

# 删除密码
time_start = time.time()
db.delete_password(db.conn, 'test1', 'test1', 'test1')
time_end = time.time()
print(f'Delete password time: {time_end - time_start}')

# 搜索关键字
time_start = time.time()
db.search_password(db.conn, 'admin', 'baidu')
time_end = time.time()
print(f'Search password time: {time_end - time_start}')
