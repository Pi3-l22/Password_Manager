import mysql.connector
from mysql.connector import Error
import logging as log

# 数据库连接参数
HOST_NAME = 'YOUR_REMOTE_DATABASE_IP'
USER_NAME = 'YOUR_REMOTE_DATABASE_USERNAME'
USER_PASSWORD = 'YOUR_REMOTE_DATABASE_PASSWORD'
DB_NAME = 'password_manager'

# 状态码
ERROR = -1
OK = 1


# 创建数据库连接
def create_connection(host_name, user_name, user_password, db_name):
    connection = None  # 初始化连接对象为None
    try:
        connection = mysql.connector.connect(
            host=host_name,  # 服务器主机名
            user=user_name,  # 数据库的用户名
            passwd=user_password,  # 用户的密码
            database=db_name  # 数据库名称
        )
        log.info('Connection to DB successful')
    except Error as e:
        log.error(f'Create connection error: {e}')
    return connection


# 关闭数据库连接
def close_connection(connection):
    if connection:
        connection.close()
        log.info('Connection closed')


# 根据用户名去用户表中查询用户信息
# 若存在用户名则返回密码，否则返回None
def query_user(connection, username):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM user WHERE username = '{username}'")
        result = cursor.fetchall()
        if len(result) == 0:
            return None
        else:
            return result[0][1]
    except Error as e:
        log.error(f'Query user error: {e}')
        return ERROR
    finally:
        cursor.close()


# 在用户表中插入用户名和密码信息
# 若插入成功则返回OK，否则返回ERROR
def insert_user(connection, username, password_hash):
    cursor = connection.cursor()
    try:
        cursor.execute(f"INSERT INTO user (username, password_hash) VALUES ('{username}', '{password_hash}')")
        connection.commit()
        return OK
    except Error as e:
        log.error(f'Insert user error: {e}')
        return ERROR
    finally:
        cursor.close()


# 在密码表中查询用户的密码信息
# 若存在则返回所有该用户的密码信息列表，否则返回None
def query_password(connection, username):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM password WHERE username = '{username}'")
        result = cursor.fetchall()
        if len(result) == 0:
            return None
        else:
            # 将该用户的所有密码信息转成字典返回
            pwd_info_list = []
            for item in result:
                pwd_info_list.append({
                    'username': item[0],
                    'website_name': item[1],
                    'website': item[2],
                    'account': item[3],
                    'password_encrypted': item[4],
                    'encrypted_method': item[5],
                    'note': item[6],
                    'created_at': item[7].strftime('%Y-%m-%d'),
                })
            return pwd_info_list
    except Error as e:
        log.error(f'Query password error: {e}')
        return ERROR
    finally:
        cursor.close()


# 在密码表中插入用户的密码信息
# 若插入成功则返回OK，否则返回ERROR
def insert_password(connection, username, website_name, website, account, password_encrypted, encrypted_method, note):
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"INSERT INTO password (username, website_name, website, account, password_encrypted, encrypted_method, note) "
            f"VALUES ('{username}', '{website_name}', '{website}', '{account}', '{password_encrypted}', '{encrypted_method}', '{note}')")
        connection.commit()
        return OK
    except Error as e:
        log.error(f'Insert password error: {e}')
        return ERROR
    finally:
        cursor.close()


# 根据用户名和网站名和账号去密码表中查询创建时间
# 若存在则返回密码信息，否则返回None
def query_password_created_at(connection, username, website_name, account):
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"SELECT created_at FROM password WHERE username = '{username}' AND website_name = '{website_name}' AND account = '{account}'")
        result = cursor.fetchall()
        if len(result) == 0:
            return None
        else:
            return result[0][0].strftime('%Y-%m-%d')

    except Error as e:
        log.error(f'Query password by website error: {e}')
        return ERROR
    finally:
        cursor.close()


# 根据用户名和网站名和账号去密码表中删除密码信息
# 若删除成功则返回OK，否则返回ERROR
def delete_password(connection, username, website_name, account):
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"DELETE FROM password WHERE username = '{username}' AND website_name = '{website_name}' AND account = '{account}'")
        connection.commit()
        return OK
    except Error as e:
        log.error(f'Delete password error: {e}')
        return ERROR
    finally:
        cursor.close()


# 根据搜索关键字去密码表中模糊搜索所有字段相关的数据
# keywords中用空格分隔的多个关键字，可以是网站名、网址、账号、备注、创建时间
# 若存在则返回密码信息列表，否则返回None
def search_password(connection, username, keywords):
    cursor = connection.cursor()
    if keywords == '':  # 若搜索关键字为空则返回所有密码信息
        return query_password(connection, username)
    else:
        keywords_list = keywords.split()
        try:
            sql = f"SELECT * FROM password WHERE username = '{username}' AND ("
            for keyword in keywords_list:
                sql += f"website_name LIKE '%{keyword}%' OR website LIKE '%{keyword}%' OR account LIKE '%{keyword}%' OR note LIKE '%{keyword}%' OR created_at LIKE '%{keyword}%' OR "
            sql = sql[:-4] + ')'
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                return None
            else:
                # 将该用户的所有密码信息转成字典返回
                pwd_info_list = []
                for item in result:
                    pwd_info_list.append({
                        'username': item[0],
                        'website_name': item[1],
                        'website': item[2],
                        'account': item[3],
                        'password_encrypted': item[4],
                        'encrypted_method': item[5],
                        'note': item[6],
                        'created_at': item[7].strftime('%Y-%m-%d'),
                    })
                return pwd_info_list
        except Error as e:
            log.error(f'Search password error: {e}')
            return ERROR
        finally:
            cursor.close()


# 创建数据库连接
conn = create_connection(HOST_NAME, USER_NAME, USER_PASSWORD, DB_NAME)
