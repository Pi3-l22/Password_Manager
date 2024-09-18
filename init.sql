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
    VALUES ('admin', 'github', 'github.com', 'github_account', 'c405475fa0dc6c2219a6bba76735d472b5f6bbfa0562b332f46fbc4b1128b3120a4b015a58a6', 'AES-256', 'AES-256');
INSERT INTO password (username, website_name, website, account, password_encrypted, encrypted_method, note) 
    VALUES ('admin', 'baidu', 'www.baidu.com', 'baidu_account', '9358b86f9f28785c62e8252552a39bdc27b4', 'ChaCha20', 'ChaCha20');
INSERT INTO password (username, website_name, website, account, password_encrypted, encrypted_method, note) 
    VALUES ('admin', 'google', 'www.google.com', 'google_account', 'ae99169a796dac2744c480b1aa11541878363d256444042ed0afe92a2970', 'XChaCha20', 'XChaCha20');
INSERT INTO password (username, website_name, website, account, password_encrypted, encrypted_method, note)
    VALUES ('admin', 'bilibili', 'www.bilibili.com', 'bilibili_account', 'rL959Ro7xjFlpLacaKFzoA==', 'SM4-ECB', 'SM4-ECB');