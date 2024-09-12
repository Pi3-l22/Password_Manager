-- Description: 初始化数据库

-- 删除数据库
-- DROP DATABASE IF EXISTS test;

-- 创建数据库
# CREATE DATABASE IF NOT EXISTS password_manager;
CREATE DATABASE IF NOT EXISTS test;

-- 使用数据库
# USE password_manager;
USE test;

-- 创建用户表
CREATE TABLE IF NOT EXISTS user (
    username VARCHAR(255) NOT NULL PRIMARY KEY,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建密码表
CREATE TABLE IF NOT EXISTS password (
    username VARCHAR(255) NOT NULL,
    website_name VARCHAR(150) NOT NULL,
    website VARCHAR(150),
    account VARCHAR(150) NOT NULL,
    password_encrypted VARCHAR(255) NOT NULL,
    encrypted_method VARCHAR(50) NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (username, website_name, account),
    FOREIGN KEY (username) REFERENCES user(username)
);
