import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, db_name):
    connection = None  # 初始化连接对象为None
    try:
        connection = mysql.connector.connect(
            host=host_name,  # 服务器主机名
            user=user_name,  # 数据库的用户名
            passwd=user_password,  # 用户的密码
            database=db_name  # 数据库名称
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def create_tables(connection):
    try:
        cur = connection.cursor()  # 获取游标对象

        # 创建 user 表
        # 该表包含 id, username, keyword, created_at, updated_at 字段
        # id 是自增主键，username 有唯一性约束
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                keyword VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
        """)

        # 创建 password 表
        # 该表包含 id, website_name, website, account, password_encrypted, note, author_id, created_at, updated_at 字段
        # id 是自增主键，author_id+website_name+account 作为联合唯一键
        # author_id 是外键，引用 user 表的 id 字段
        # website_name 有唯一性约束
        cur.execute("""
            CREATE TABLE IF NOT EXISTS password (
                id INT AUTO_INCREMENT PRIMARY KEY,
                website_name VARCHAR(150) NOT NULL,
                website VARCHAR(150) ,
                account VARCHAR(150) NOT NULL,
                password_encrypted VARCHAR(255) NOT NULL,
                note TEXT,
                author_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_record (author_id, website_name, account),
                FOREIGN KEY (author_id) REFERENCES user(id)
            );
        """)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def add_user(connection, username, keyword):
    query = "INSERT INTO user (username, keyword) VALUES (%s, %s)"
    data = (username, keyword)
    cur = connection.cursor()
    try:
        cur.execute(query, data)
        connection.commit()
        return cur.lastrowid  # 返回新插入行的ID
    except Error as e:
        print(f"The error '{e}' occurred")


def add_password(connection, website_name, website, account, password_encrypted, note, username):
    cur = connection.cursor()
    try:
        # 先查询用户ID
        cur.execute("SELECT id FROM user WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            author_id = user[0]
            query = """
                INSERT INTO password (website_name, website, account, password_encrypted, note, author_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = (website_name, website, account, password_encrypted, note, author_id)
            cur.execute(query, data)
            connection.commit()
            print("Password added successfully.")
        else:
            print("User not found.")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cur.close()


def delete_user(connection, username):
    """
    根据用户名从用户表里删除用户
    :param connection:
    :param username:
    :return:
    """
    cur = connection.cursor()
    try:
        # 先查询用户ID
        cur.execute("SELECT id FROM user WHERE username = %s", (username,))
        user_id = cur.fetchone()
        if user_id:
            user_id = user_id[0]
            # 删除用户
            cur.execute("DELETE FROM user WHERE id = %s", (user_id,))
            connection.commit()
            print("User deleted successfully.")
        else:
            print("User not found.")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cur.close()


def delete_password(connection, username, website_name):
    """
    根据用户名和网站名称从密码表里删除密码信息
    :param connection:
    :param username:
    :param website_name:
    :return:
    """
    cur = connection.cursor()
    try:
        # 先查询用户ID
        cur.execute("SELECT id FROM user WHERE username = %s", (username,))
        user_id = cur.fetchone()
        if user_id:
            user_id = user_id[0]
            # 删除密码信息
            cur.execute("DELETE FROM password WHERE author_id = %s AND website_name = %s", (user_id, website_name))
            connection.commit()
            print("Passwords deleted successfully.")
        else:
            print("User not found.")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cur.close()


def update_user(connection, new_username, new_keyword, username):
    """
    根据用户名修改用户表
    :param connection:
    :param new_username:
    :param new_keyword:
    :param username:
    :return:
    """
    cur = connection.cursor()
    try:
        # 查询用户ID
        cur.execute("SELECT id FROM user WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            user_id = user[0]
            # 更新用户信息
            cur.execute("UPDATE user SET username = %s, keyword = %s WHERE id = %s", (new_username, new_keyword, user_id))
            connection.commit()
            print("User updated successfully.")
        else:
            print("User not found.")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cur.close()


def update_password(connection, username, website_name, new_website, new_account, new_password_encrypted, new_note):
    """
    根据用户名和网站名称更改密码表
    :param connection:
    :param username:
    :param website_name:
    :param new_website:
    :param new_account:
    :param new_password_encrypted:
    :param new_note:
    :return:
    """
    cur = connection.cursor()
    try:
        # 查询用户ID
        cur.execute("SELECT id FROM user WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            user_id = user[0]
            # 查询密码记录是否存在
            cur.execute("SELECT id FROM password WHERE author_id = %s AND website_name = %s", (user_id, website_name))
            password = cur.fetchone()
            if password:
                password_id = password[0]
                # 更新密码信息
                cur.execute(
                    "UPDATE password SET website = %s, account = %s, password_encrypted = %s, note = %s "
                    "WHERE author_id = %s AND website_name = %s",
                    (new_website, new_account, new_password_encrypted, new_note, user_id, website_name))
                connection.commit()
                print("Password updated successfully.")
            else:
                print("Password record not found.")
        else:
            print("User not found.")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cur.close()


def select_all_users(connection):
    query = "SELECT * FROM user"
    cur = connection.cursor()
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        print(row)


def select_all_passwords(connection):
    query = "SELECT * FROM password"
    cur = connection.cursor()
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        print(row)


def query_password(connection, username, website_name):
    """
    根据用户名和网站名称从密码表里查询密码信息
    :param connection:
    :param username:
    :param website_name:
    :return:
    """
    cur = connection.cursor()
    query = """
        SELECT * FROM password
        WHERE author_id = (SELECT id FROM user WHERE username = %s) AND website_name = %s
    """
    cur.execute(query, (username, website_name))
    records = cur.fetchall()
    for row in records:
        print(row)


def search_passwords(connection, search_keyword):
    """
    模糊搜索功能
    :param connection:
    :param search_keyword:
    :return:
    """
    cur = connection.cursor()
    try:
        # 使用 LIKE 进行模糊搜索
        query = """
            SELECT p.id, p.website_name, p.website, p.account, p.password_encrypted, p.note, u.username
            FROM password p
            JOIN user u ON p.author_id = u.id
            WHERE p.website_name LIKE %s OR p.website LIKE %s OR p.account LIKE %s
            OR p.password_encrypted LIKE %s OR p.note LIKE %s
        """
        cur.execute(query, ('%' + search_keyword + '%', '%' + search_keyword + '%', '%' + search_keyword + '%', '%' + search_keyword + '%', '%' + search_keyword + '%'))
        records = cur.fetchall()
        if records:
            print(f"Found {len(records)} records:")
            for row in records:
                print(row)
        else:
            print("No records found.")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cur.close()


def main():
    host_name = '127.0.0.1'
    user_name = 'user'
    user_password = '123456'
    db_name = 'test'

    # create a database connection
    connection = create_connection(host_name, user_name, user_password, db_name)

    if connection is not None and connection.is_connected():
        create_tables(connection)

        # 用户选择操作
        while True:
            print("\nOptions:")
            print("A. Add")
            print("B. Delete")
            print("C. Query")
            print("D. Modify")
            print("E. Exit")
            choice = input("Enter your choice: ").upper()

            if choice == 'A':
                print("\nAdd options:")
                print("1. Add a user")
                print("2. Add a password")
                add_choice = input("Enter your choice: ")
                if add_choice == '1':
                    username = input("Enter username: ")
                    keyword = input("Enter password: ")
                    user_id = add_user(connection, username, keyword)
                    print(f"User added with ID: {user_id}")
                elif add_choice == '2':
                    website_name = input("Enter website name: ")
                    website = input("Enter website: ")
                    account = input("Enter account: ")
                    password_encrypted = input("Enter encrypted password: ")
                    note = input("Enter note: ")
                    username = input("Enter username: ")
                    add_password(connection, website_name, website, account, password_encrypted, note, username)
                else:
                    print("Invalid choice. Please choose a valid option.")

            elif choice == 'B':
                print("\nDelete options:")
                print("1. Delete user by username")
                print("2. Delete password by username and website name")
                delete_choice = input("Enter your choice: ")
                if delete_choice == '1':
                    username = input("Enter username to delete: ")
                    delete_user(connection, username)
                elif delete_choice == '2':
                    username = input("Enter username to delete password: ")
                    website_name = input("Enter website name to delete password: ")
                    delete_password(connection, username, website_name)
                else:
                    print("Invalid choice. Please choose a valid option.")

            elif choice == 'C':
                print("\nQuery options:")
                print("1. View user table")
                print("2. View password table")
                print("3. Query password by username and website name")
                print("4. Fuzzy search")
                query_choice = input("Enter your choice: ")
                if query_choice == '1':
                    select_all_users(connection)
                elif query_choice == '2':
                    select_all_passwords(connection)
                elif query_choice == '3':
                    username = input("Enter username to query password: ")
                    website_name = input("Enter website name to query password: ")
                    query_password(connection, username, website_name)
                elif query_choice == '4':
                    search_keyword = input("Enter search keyword: ")
                    search_passwords(connection, search_keyword)
                else:
                    print("Invalid choice. Please choose a valid option.")

            elif choice == 'D':
                print("\nModify options:")
                print("1. Update user by username")
                print("2. Update password by username and website name")
                modify_choice = input("Enter your choice: ")
                if modify_choice == '1':
                    username = input("Enter username to update: ")
                    new_username = input("Enter new username: ")
                    new_keyword = input("Enter new password: ")
                    update_user(connection, new_username, new_keyword, username)
                elif modify_choice == '2':
                    username = input("Enter username: ")
                    website_name = input("Enter website name: ")
                    new_website = input("Enter new website: ")
                    new_account = input("Enter new account: ")
                    new_password_encrypted = input("Enter new encrypted password: ")
                    new_note = input("Enter new note: ")
                    update_password(connection, username, website_name, new_website, new_account, new_password_encrypted, new_note)
                else:
                    print("Invalid choice. Please choose a valid option.")

            elif choice == 'E':
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please choose a valid option.")
    else:
        print("Error! cannot create the database connection.")

    if connection and connection.is_connected():
        connection.close()


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
