# 密码管理器

[English](README.md) | [简体中文](README_CN.md)

一个使用Python和Flet构建的安全、用户友好的密码管理应用程序。

项目详细介绍请见我的博客：[Pi3'Notes](https://blog.pi3.fun/post/2024/09/%E5%AF%86%E7%A0%81%E7%AE%A1%E7%90%86%E5%99%A8%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1%E4%B8%8E%E5%AE%9E%E7%8E%B0/)

## 功能特性

- 安全的用户认证
- 使用多种算法加密存储密码（AES-256、ChaCha20、XChaCha20、SM4-ECB）
- 添加、查看、编辑和删除密码条目
- 搜索功能，快速访问存储的密码
- 支持多种格式（JSON、CSV、TXT）导入和导出密码数据
- 随机强密码生成器
- 支持暗黑模式

## 使用的技术

- Python 3.x
- Flet（GUI框架）
- MySQL（数据库）
- Cryptodome（加密库）
- pysm4（SM4加密）

## 安装

1. 克隆仓库：
   ```
   git clone https://github.com/Pi3-l22/Password_Manager.git
   ```

2. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

3. 设置MySQL数据库并更新`database_op.py`中的连接详情：
   ```python
   HOST_NAME = '你的远程数据库IP'
   USER_NAME = '你的远程数据库用户名'
   USER_PASSWORD = '你的远程数据库密码'
   DB_NAME = 'password_manager'
   ```

4. 运行应用程序：
   ```
   python main.py
   ```

5. 运行Web应用程序：
   ```
   python web/main.py
   ```

程序运行后，在浏览器中访问`http://IP:8000`即可访问Web应用程序。

6. (可选) 打包成桌面应用程序：
   ```
    flet pack main.py --add-data "asset;asset" --icon "D:\Desktop\PassWordManager\asset\logo.ico" 
    --product-name "PassManager"  --product-version "1.0" --file-version "1.0" 
    --file-description "A simple and safe password manager" --copyright "By Pi3"
   ```

## 使用方法

1. 启动应用程序，创建新用户账户或使用现有凭据登录。
2. 使用直观的界面管理你的密码：
   - 添加新的密码条目
   - 查看和编辑现有条目
   - 删除不需要的条目
   - 搜索特定密码
3. 根据需要导入或导出密码数据。
4. 使用随机密码生成器创建强大、唯一的密码。

## 安全性

- 用户密码在存储前使用SHA3-256进行哈希处理。
- 存储的密码使用用户选择的AES-256、ChaCha20、XChaCha20或SM4-ECB算法进行加密。
- 加密密钥使用PBKDF2进行10,000次迭代派生，以增加安全性。

## 许可证

本项目采用MIT许可证 - 详情请见[MIT LICENSE](LICENSE)文件。

## 致谢

- [Flet](https://flet.dev/)提供GUI框架
- [Cryptodome](https://www.pycryptodome.org/)提供加密算法
- [pysm4](https://github.com/zjwei/pysm4)提供SM4加密支持
