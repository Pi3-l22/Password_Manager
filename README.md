# Password Manager

[English](README.md) | [简体中文](README_CN.md)

A secure and user-friendly password management application built with Python and Flet.

For a detailed project description, please visit my blog: [Pi3's Notes](https://blog.pi3.fun/post/2024/09/%E5%AF%86%E7%A0%81%E7%AE%A1%E7%90%86%E5%99%A8%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1%E4%B8%8E%E5%AE%9E%E7%8E%B0/)

## Features

- Secure user authentication
- Password storage with multiple encryption algorithms (AES-256, ChaCha20, XChaCha20, SM4-ECB)
- Add, view, edit, and delete password entries
- Search functionality for quick access to stored passwords
- Import and export password data in various formats (JSON, CSV, TXT)
- Random strong password generator
- Dark mode support

## Technologies Used

- Python 3.x
- Flet (GUI framework)
- MySQL (database)
- Cryptodome (encryption library)
- pysm4 (SM4 encryption)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Pi3-l22/Password_Manager.git
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up MySQL database and update connection details in `database_op.py`:
   ```python
   HOST_NAME = 'your_remote_database_ip'
   USER_NAME = 'your_remote_database_username'
   USER_PASSWORD = 'your_remote_database_password'
   DB_NAME = 'password_manager'
   ```

4. Run the application:
   ```
   python main.py
   ```

5. Run the Web application:
   ```
   python web/main.py
   ```

After running the program, access the Web application by visiting `http://IP:8000` in your browser.

6. (Optional) Package as a desktop application:
   ```
    flet pack main.py --add-data "asset;asset" --icon "D:\Desktop\PassWordManager\asset\logo.ico" 
    --product-name "PassManager"  --product-version "1.0" --file-version "1.0" 
    --file-description "A simple and safe password manager" --copyright "By Pi3"
   ```

## Usage

1. Launch the application, create a new user account or log in with existing credentials.
2. Use the intuitive interface to manage your passwords:
   - Add new password entries
   - View and edit existing entries
   - Delete unwanted entries
   - Search for specific passwords
3. Import or export password data as needed.
4. Use the random password generator to create strong, unique passwords.

## Security

- User passwords are hashed using SHA3-256 before storage.
- Stored passwords are encrypted using user-selected AES-256, ChaCha20, XChaCha20, or SM4-ECB algorithms.
- Encryption keys are derived using PBKDF2 with 10,000 iterations for added security.

## License

This project is licensed under the MIT License - see the [MIT LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flet](https://flet.dev/) for the GUI framework
- [Cryptodome](https://www.pycryptodome.org/) for encryption algorithms
- [pysm4](https://github.com/zjwei/pysm4) for SM4 encryption support
