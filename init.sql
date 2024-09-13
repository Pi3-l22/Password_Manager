-- Description: 初始化数据库

-- 删除数据库
-- DROP DATABASE IF EXISTS test;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS password_manager;
-- CREATE DATABASE IF NOT EXISTS test;

-- 使用数据库
USE password_manager;
-- USE test;

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
    PRIMARY KEY (username, website_name, account),
    FOREIGN KEY (username) REFERENCES user(username)
);


-- 创建例子数据
INSERT INTO user (username, password_hash) VALUES ('admin', 'fb001dfcffd1c899f3297871406242f097aecf1a5342ccf3ebcd116146188e4b');
INSERT INTO password (username, website_name, website, account, password_encrypted, encrypted_method, note) 
    VALUES ('admin', 'github', 'https://github.com', 'github_account', 'c397a131306195d62732b6dc6f806987f99265c35ae8b7a344c68f60df51df5938e8ca013125', 'AES-256', '使用AES-256加密');
INSERT INTO password (username, website_name, website, account, password_encrypted, encrypted_method, note) 
    VALUES ('admin', 'baidu', 'https://www.baidu.com', 'baidu_account', '9c312737378ec4d374b9c05d20cf4b0340ab', 'ChaCha20', '使用ChaCha20加密');
INSERT INTO password (username, website_name, website, account, password_encrypted, encrypted_method, note) 
    VALUES ('admin', 'google', 'https://www.google.com', 'google_account', '0e27e8028aa4fd92d0de5ae2da53fa06f5200af8bdacfda18bc04c7f1fbd', 'XChaCha20', '使用XChaCha20加密');