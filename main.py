import flet as ft
import pyperclip
from gvcode import VFCode
import data_encrypt as de
import database_op as db

# 全局主题变量
BGCOLOR = '#f0f0f0'
THEME = ft.ThemeMode.LIGHT


# 登录页面类
class LoginPage(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        # 主标题
        self.title = ft.Stack(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "密码管理器",
                            ft.TextStyle(
                                size=50,
                                weight=ft.FontWeight.BOLD,
                                letter_spacing=25,
                                foreground=ft.Paint(
                                    color="#0C6CC9",
                                    stroke_width=8,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "密码管理器",
                            ft.TextStyle(
                                size=50,
                                weight=ft.FontWeight.BOLD,
                                letter_spacing=25,
                                color="#EDF5F8",
                            ),
                        ),
                    ],
                ),
            ]
        )

        # logo图片
        # self.logo_image = ft.Image(
        #     # src="asset/image/lock.png",
        #     src="image/lock.png",
        #     width=100,
        #     height=100,
        # )

        # 用户名和密码输入框
        self.password_box = ft.TextField(
            label="Password",
            hint_text="请输入你的主密码",
            max_lines=1,
            width=350,
            height=55,
            password=True,
            can_reveal_password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            shift_enter=True,
            on_submit=self.btn_login_click
        )
        self.username_box = ft.TextField(
            label="Username",
            hint_text="请输入你的用户名",
            max_lines=1,
            width=350,
            height=55,
            autofocus=True,
            shift_enter=True,
            on_submit=lambda e: self.password_box.focus(),
        )

        # 登录和注册按钮
        self.btn_login = ft.ElevatedButton(
            text="登入",
            width=150,
            height=50,
            animate_size=True,
            on_click=self.btn_login_click,
            icon=ft.icons.LOGIN,
        )
        self.btn_register = ft.ElevatedButton(
            text="注册",
            width=150,
            height=50,
            animate_size=True,
            on_click=self.btn_register_click,
            icon=ft.icons.PERSON_ADD_ALT,
        )

        # 登录事件错误弹窗
        self.w_pwd_dlg = ft.AlertDialog(
            title=ft.Text("用户名或密码错误", weight=ft.FontWeight.BOLD),
            content=ft.Text("请检查你的用户名和密码是否正确!"),
        )
        self.w_no_user_dlg = ft.AlertDialog(
            title=ft.Text("用户名或密码为空", weight=ft.FontWeight.BOLD),
            content=ft.Text("请输入你的用户名和密码!"),
        )
        # 在页面上添加弹窗
        self.page.overlay.extend([self.w_pwd_dlg, self.w_no_user_dlg])

        # 添加控件
        self.controls = [
            ft.Row(
                [
                    self.title,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    # self.logo_image,
                    ft.Icon(name=ft.icons.LOCK, size=100, color=ft.colors.BLUE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    self.username_box,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    self.password_box,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    self.btn_login,
                    self.btn_register,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=50,
            ),

        ]
        self.spacing = 20
        self.alignment = ft.MainAxisAlignment.CENTER
        self.code = ""  # 验证码

    # 登录按钮点击事件
    def btn_login_click(self, e):
        if self.username_box.value == "" or self.password_box.value == "":
            # self.page.overlay.append(self.w_no_user_dlg)
            self.w_no_user_dlg.open = True
            self.page.update()
        else:
            # 数据库操作
            password = db.query_user(db.conn, self.username_box.value)
            if password is not None:
                if password == de.sha3_256(self.password_box.value):
                    current_user = self.username_box.value
                    current_key = self.password_box.value
                    main_page(self.page, current_user, current_key)
                else:
                    # self.page.overlay.append(self.w_pwd_dlg)
                    self.w_pwd_dlg.open = True
                    self.page.update()
            else:
                # self.page.overlay.append(self.w_pwd_dlg)
                self.w_pwd_dlg.open = True
                self.page.update()

    # 注册按钮点击事件
    def btn_register_click(self, e):
        Register_page(self.page)


# 注册页面类
class RegisterPage(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        # 生成验证码
        vc = VFCode()
        vc.generate_digit(4)
        self.code = vc.code
        vc.save(f"{self.code}.png")
        # 标题
        self.title = ft.Text("注册用户", size=40, weight=ft.FontWeight.BOLD)  # color='#043D79'
        # 用户名和密码输入框
        self.password_box = ft.TextField(
            label="主密码",
            hint_text="请输入你的主密码",
            max_lines=1,
            width=350,
            height=55,
            password=True,
            can_reveal_password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            shift_enter=True,
            on_submit=self.register_click
        )
        self.username_box = ft.TextField(
            label="用户名",
            hint_text="请输入你的用户名",
            max_lines=1,
            width=350,
            height=55,
            autofocus=True,
            shift_enter=True,
            on_submit=lambda e: self.password_box.focus(),
        )
        # 验证码
        self.vf_code = ft.Row(
            [
                ft.TextField(
                    label="验证码",
                    max_lines=1,
                    width=200,
                    height=50,
                ),
                ft.Image(
                    src=f"{self.code}.png",
                    width=125,
                    height=50,
                ),
            ],
            spacing=25
        )
        # 登录和注册按钮
        self.btn_cancel = ft.OutlinedButton(
            text="取消",
            width=150,
            height=50,
            animate_size=True,
            on_click=self.cancel_click,
            icon=ft.icons.CANCEL_OUTLINED,
        )
        self.btn_register = ft.OutlinedButton(
            text="注册",
            width=150,
            height=50,
            animate_size=True,
            on_click=self.register_click,
            icon=ft.icons.PERSON_ADD_ALT,
        )

        # 添加控件
        self.controls = [
            ft.Row(
                [
                    self.title,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    self.username_box,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    self.password_box,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    self.vf_code,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    self.btn_register,
                    self.btn_cancel,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=50,
            ),
        ]
        self.spacing = 25

        # 注册事件错误弹窗
        self.w_register_dlg = ft.AlertDialog(
            title=ft.Text("用户名已存在", weight=ft.FontWeight.BOLD),
            content=ft.Text("请重新输入用户名！"),
        )
        self.w_vf_code_dlg = ft.AlertDialog(
            title=ft.Text("验证码错误", weight=ft.FontWeight.BOLD),
            content=ft.Text("请重新输入验证码！"),
        )
        self.w_no_user_dlg = ft.AlertDialog(
            title=ft.Text("用户名和密码为空", weight=ft.FontWeight.BOLD),
            content=ft.Text("请输入用户名和密码！"),
        )
        # 注册成功弹窗
        self.register_success_dlg = ft.AlertDialog(
            title=ft.Text("注册成功", weight=ft.FontWeight.BOLD),
            content=ft.Text("请继续完成登录操作"),
        )
        # 在页面上添加弹窗
        self.page.overlay.extend(
            [self.w_register_dlg, self.w_vf_code_dlg, self.w_no_user_dlg, self.register_success_dlg])

    # 注册按钮事件
    def register_click(self, e):
        if self.username_box.value == "" or self.password_box.value == "":
            # self.page.overlay.append(self.w_no_user_dlg)
            self.w_no_user_dlg.open = True
            self.page.update()
        else:
            if self.vf_code.controls[0].value != self.code:
                # self.page.overlay.append(self.w_vf_code_dlg)
                self.w_vf_code_dlg.open = True
                # 重新生成验证码
                # 删除验证码图片
                import os
                if os.path.exists(f"{self.code}.png"):
                    os.remove(f"{self.code}.png")
                # 生成验证码
                vc = VFCode()
                vc.generate_digit(4)
                self.code = vc.code
                vc.save(f"{self.code}.png")
                self.vf_code.controls[1].src = f"{self.code}.png"
                self.page.update()
            else:
                # 数据库操作
                password = db.query_user(db.conn, self.username_box.value)
                if password is None:
                    db.insert_user(db.conn, self.username_box.value, de.sha3_256(self.password_box.value))
                    # self.page.overlay.append(self.register_success_dlg)
                    self.register_success_dlg.open = True
                    self.page.update()
                    main(self.page)
                    # 删除验证码图片
                    import os
                    if os.path.exists(f"{self.code}.png"):
                        os.remove(f"{self.code}.png")
                else:
                    # self.page.overlay.append(self.w_register_dlg)
                    self.w_register_dlg.open = True
                    self.page.update()

    # 取消按钮事件
    def cancel_click(self, e):
        # 删除验证码图片
        import os
        if os.path.exists(f"{self.code}.png"):
            os.remove(f"{self.code}.png")
        main(self.page)


# 添加密码信息弹窗类
class AddPwdDialog(ft.AlertDialog):
    def __init__(self, current_user, current_key, pwd_table_rows, delete_pwd_row, copy_cell, info_snack_bar):
        super().__init__()
        self.current_user = current_user
        self.current_key = current_key
        self.pwd_table_rows = pwd_table_rows
        self.delete_pwd_row = delete_pwd_row
        self.copy_cell = copy_cell
        self.info_snack_bar = info_snack_bar
        self.modal = True
        self.title = ft.Text("添加新密码信息", weight=ft.FontWeight.BOLD)
        self.content = ft.Column(
            [
                ft.TextField(
                    label="名称",
                    hint_text="请输入名称",
                    max_lines=1,
                    width=500,
                    height=55,
                    autofocus=True,
                    on_submit=lambda e: self.content.controls[1].focus(),
                ),
                ft.TextField(
                    label="账号",
                    hint_text="请输入账号",
                    max_lines=1,
                    width=500,
                    height=55,
                    on_submit=lambda e: self.content.controls[2].focus(),
                ),
                ft.TextField(
                    label="密码",
                    hint_text="请输入密码",
                    max_lines=1,
                    width=500,
                    height=55,
                    on_submit=lambda e: self.content.controls[3].focus(),
                ),
                ft.TextField(
                    label="网址",
                    hint_text="请输入网址",
                    max_lines=1,
                    width=500,
                    height=55,
                    prefix_text="https://",
                    on_submit=lambda e: self.content.controls[4].focus(),
                ),
                ft.TextField(
                    label="备注",
                    hint_text="请输入备注",
                    max_lines=1,
                    width=500,
                    height=55,
                ),
                ft.Dropdown(
                    width=500,
                    label="加密方式",
                    hint_text="请选择加密方式",
                    options=[
                        ft.dropdown.Option("AES-256 (更安全)"),
                        ft.dropdown.Option("ChaCha20 (更高效)"),
                        ft.dropdown.Option("XChaCha20 (安全且高效)"),
                        ft.dropdown.Option("SM4-ECB (国密算法)"),
                    ],
                ),
            ],
            width=500,
            height=500,
            spacing=25,
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.actions = [
            ft.IconButton(
                icon=ft.icons.KEY_ROUNDED,
                tooltip="随机生成强密码",
                on_click=self.add_random_pwd,
            ),
            ft.OutlinedButton(
                text="保存",
                on_click=self.add_pwn_dlg_save
            ),
            ft.OutlinedButton(
                text="取消",
                on_click=self.add_pwn_dlg_cancel
            ),
        ]

    # 随机生成强密码
    def add_random_pwd(self, e):
        random_pwd = de.random_password(16)
        self.content.controls[2].value = random_pwd
        self.page.update()

    # 添加密码信息弹窗取消按钮
    def add_pwn_dlg_cancel(self, e):
        self.page.close(self)
        self.page.overlay.remove(self)

    # 添加密码信息弹窗保存按钮
    def add_pwn_dlg_save(self, e):
        # 获取输入框信息
        website_name = self.content.controls[0].value
        account = self.content.controls[1].value
        password = self.content.controls[2].value
        website = self.content.controls[3].value
        note = self.content.controls[4].value
        encrypted_method = self.content.controls[5].value
        # 验证是否为空
        if website_name == "" or account == "" or password == "" or encrypted_method == "" or website == "" or note == "":
            self.info_snack_bar.content.value = "请填写完整信息!"
            self.info_snack_bar.open = True
            # self.page.close(self)
            # self.page.overlay.remove(self)
            self.page.update()
            return
        # 数据加密
        # password_encrypted = de.data_encrypt(password, de.sha_256(self.current_key), encrypted_method)
        password_encrypted = de.data_encrypt(password, de.pbkdf2(self.current_key), encrypted_method)
        # 数据库操作
        status = db.insert_password(db.conn, self.current_user, website_name, website, account, password_encrypted,
                                    encrypted_method, note)
        # 取出最新添加的密码的创建时间
        if status == 1:
            created_at = db.query_password_created_at(db.conn, self.current_user, website_name, account)
            pwd_info = PwdRow(
                cells=[
                    ft.DataCell(ft.Text(f"{website_name}"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text(f"{account}"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text(f"{password}"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text(f"{website}"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text(f"{note}"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text(f"{created_at}"), on_tap=self.copy_cell),
                ],
                delete_pwd_row=self.delete_pwd_row
            )
            self.pwd_table_rows.append(pwd_info)
            self.page.update()
            self.page.close(self)
            self.page.overlay.remove(self)
        else:
            self.info_snack_bar.content.value = "添加失败! 请检查你的输入信息是否正确!"
            self.info_snack_bar.open = True
            self.page.update()
            self.page.close(self)
            self.page.overlay.remove(self)


# 密码信息类
class PwdRow(ft.DataRow):
    def __init__(self, cells, delete_pwd_row):
        super().__init__(cells)
        self.delete_pwd_row = delete_pwd_row
        cells.append(ft.DataCell(ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED, on_click=self.delete_click)))

        # 密码信息
        self.name = cells[0].content.value
        self.account = cells[1].content.value
        self.password = cells[2].content.value
        self.remark = cells[3].content.value
        self.date = cells[4].content.value

        # 删除密码信息弹窗
        self.del_dlg = ft.AlertDialog(
            title=ft.Text("删除密码信息", weight=ft.FontWeight.BOLD),
            content=ft.Text("你确定要删除这条密码信息吗?"),
            actions=[
                ft.OutlinedButton(
                    text="确定",
                    on_click=self.del_dlg_confirm
                ),
                ft.OutlinedButton(
                    text="取消",
                    on_click=self.del_dlg_cancel
                ),
            ]
        )

    # 点击删除按钮
    def delete_click(self, e):
        self.page.overlay.append(self.del_dlg)
        self.del_dlg.open = True
        self.page.update()

    # 删除密码信息弹窗取消按钮
    def del_dlg_cancel(self, e):
        self.page.close(self.del_dlg)

    # 删除密码信息弹窗确定按钮
    def del_dlg_confirm(self, e):
        self.page.close(self.del_dlg)
        self.delete_pwd_row(self)


# 主页面对象
class MainPage(ft.Column):
    def __init__(self, current_user, current_key, page):
        super().__init__()
        self.page = page
        self.current_user = current_user
        self.current_key = current_key
        # 添加密码按钮
        self.btn_add_pwd = ft.IconButton(
            icon=ft.icons.ADD_CIRCLE,
            icon_size=50,
            tooltip="添加新的密码信息",
            on_click=self.btn_add_pwd_click,
        )

        # 搜索框
        self.search_box = ft.SearchBar(
            bar_hint_text="输入关键字搜索",
            on_submit=self.search_box_submit,
            width=600,
        )

        # 搜索提交按钮
        self.btn_search = ft.IconButton(
            icon=ft.icons.SEARCH,
            icon_size=50,
            tooltip="搜索关键字信息",
            on_click=self.search_box_submit,
        )

        # 批量导入按钮
        self.btn_import = ft.IconButton(
            icon=ft.icons.FILE_OPEN_ROUNDED,
            icon_size=50,
            tooltip="批量导入密码信息",
            on_click=self.import_pwd_click,
        )

        # 批量导出按钮
        self.btn_export = ft.IconButton(
            icon=ft.icons.UPLOAD_FILE_ROUNDED,
            icon_size=50,
            tooltip="批量导出密码信息",
            on_click=self.export_pwd_click,
        )

        # BUG
        # 退出当前用户按钮
        self.btn_logout = ft.IconButton(
            icon=ft.icons.LOGOUT,
            icon_size=50,
            tooltip="退出当前用户",
            on_click=lambda _: main(self.page),
        )

        # 切换明暗模式按钮
        self.btn_change_theme = ft.IconButton(
            icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
            icon_size=50,
            tooltip="切换明暗模式",
            on_click=lambda _: change_theme(self.page),
        )

        # 密码信息表
        self.pwd_table = ft.DataTable(
            width=1100,
            bgcolor='#44C0DDEE',
            border_radius=20,
            heading_text_style=ft.TextStyle(weight=ft.FontWeight.W_900, size=16),  # color="#043D79"
            # column_spacing=20,
            columns=[
                ft.DataColumn(ft.Text("名称")),
                ft.DataColumn(ft.Text("账号")),
                ft.DataColumn(ft.Text("密码")),
                ft.DataColumn(ft.Text("网址")),
                ft.DataColumn(ft.Text("备注")),
                ft.DataColumn(ft.Text("创建日期")),
                ft.DataColumn(ft.Text("删除")),
            ],
            rows=[],
        )

        # 密码信息展示
        self.pwd_lists = ft.Column(
            height=535,
            width=1100,
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.pwd_table,
            ]
        )

        # 添加控件
        self.controls = [
            ft.Row(
                [
                    self.btn_change_theme,
                    self.btn_add_pwd,
                    self.search_box,
                    self.btn_search,
                    self.btn_import,
                    self.btn_export,
                    self.btn_logout,
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [
                    self.pwd_lists,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]
        self.spacing = 20

        # 自动创建密码信息对象
        # 数据库查询用户所有数据
        pwd_list = db.query_password(db.conn, self.current_user)
        if pwd_list is not None:
            for pwd in pwd_list:
                # key = de.sha_256(self.current_key)
                key = de.pbkdf2(self.current_key)
                password = de.data_decrypt(pwd['password_encrypted'], key, pwd['encrypted_method'])
                pwd_info = PwdRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{pwd['website_name']}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{pwd['account']}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{password}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{pwd['website']}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{pwd['note']}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{pwd['created_at']}"), on_tap=self.copy_cell),
                    ],
                    delete_pwd_row=self.delete_pwd_row
                )
                self.pwd_table.rows.append(pwd_info)

        # 密码数据导入文件路径
        self.local_file_path = ""
        # 密码数据导出目录路径
        self.local_dir_path = ""
        # 目录选择弹窗
        self.get_directory_dialog = ft.FilePicker(on_result=self.get_directory_result)
        # 文件选择弹窗
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.extend([self.get_directory_dialog, self.pick_files_dialog])
        # 底部信息弹窗
        self.info_snack_bar = ft.SnackBar(ft.Text(), duration=2000)
        self.page.overlay.append(self.info_snack_bar)
        # 导出密码信息弹窗
        self.choose_export_dlg = ft.AlertDialog(
            title=ft.Text("导出所有密码数据", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.TextField(
                                label="目录",
                                hint_text="请选择保存目录",
                                max_lines=1,
                                width=280,
                                height=55,
                                autofocus=True,
                            ),
                            ft.IconButton(
                                icon=ft.icons.CREATE_NEW_FOLDER,
                                icon_size=40,
                                on_click=lambda _: self.get_directory_dialog.get_directory_path(
                                    dialog_title="选择一个保存目录", )
                            )
                        ],
                        spacing=10
                    ),
                    ft.Dropdown(
                        width=280,
                        label="导出格式",
                        hint_text="请选择加密方式",
                        options=[
                            ft.dropdown.Option("JSON"),
                            ft.dropdown.Option("CSV"),
                            ft.dropdown.Option("TXT"),
                        ],
                    ),
                ],
                width=350,
                height=180,
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.OutlinedButton(
                    text="导出",
                    on_click=self.export_pwd_dlg_save
                ),
                ft.OutlinedButton(
                    text="取消",
                    on_click=self.export_pwd_dlg_cancel
                ),
            ],
            modal=True
        )
        # 导入密码信息弹窗
        self.choose_import_dlg = ft.AlertDialog(
            title=ft.Text("导入密码数据", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.TextField(
                                label="文件",
                                hint_text="请选择文件路径",
                                max_lines=1,
                                width=280,
                                height=55,
                                autofocus=True,
                            ),
                            ft.IconButton(
                                icon=ft.icons.FILE_PRESENT_ROUNDED,
                                icon_size=40,
                                on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=False),
                            )
                        ],
                        spacing=10
                    ),
                ],
                width=350,
                height=100,
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.OutlinedButton(
                    text="导入",
                    on_click=self.import_pwd_dlg_save
                ),
                ft.OutlinedButton(
                    text="取消",
                    on_click=self.import_pwd_dlg_cancel
                ),
            ],
            modal=True
        )
        # 在页面中添加导入导出弹窗控件
        self.page.overlay.extend([self.choose_export_dlg, self.choose_import_dlg])

    # 添加密码按钮点击事件
    def btn_add_pwd_click(self, e):
        # 创建添加密码信息弹窗对象
        add_pwd_dlg = AddPwdDialog(self.current_user, self.current_key, self.pwd_table.rows, self.delete_pwd_row,
                                   self.copy_cell, self.info_snack_bar)
        self.page.overlay.append(add_pwd_dlg)
        add_pwd_dlg.open = True
        self.page.update()

    # 搜索框提交事件
    def search_box_submit(self, e):
        keywords = self.search_box.value
        # 数据库操作
        pwd_list = db.search_password(db.conn, self.current_user, keywords)
        if pwd_list is not None:
            self.pwd_table.rows.clear()
            for pwd in pwd_list:
                # key = de.sha_256(self.current_key)
                key = de.pbkdf2(self.current_key)
                password = de.data_decrypt(pwd['password_encrypted'], key, pwd['encrypted_method'])
                pwd_info = PwdRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{pwd['website_name']}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{pwd['account']}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{password}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{pwd['website']}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{pwd['note']}"), on_tap=self.copy_cell),
                        ft.DataCell(ft.Text(f"{pwd['created_at']}"), on_tap=self.copy_cell),
                    ],
                    delete_pwd_row=self.delete_pwd_row
                )
                self.pwd_table.rows.append(pwd_info)
            self.page.update()
        else:
            self.info_snack_bar.content.value = "搜索失败! 未找到相关信息!"
            self.info_snack_bar.open = True
            self.page.update()

    # 删除密码表格信息
    def delete_pwd_row(self, pwd_row):
        # 数据库操作
        website_name = pwd_row.cells[0].content.value
        account = pwd_row.cells[1].content.value
        status = db.delete_password(db.conn, self.current_user, website_name, account)
        if status == 1:
            self.pwd_table.rows.remove(pwd_row)
            self.update()
        else:
            self.info_snack_bar.content.value = "删除失败! 请检查你的操作是否正确!"
            self.info_snack_bar.open = True
            self.page.update()

    # 复制单元格内容
    def copy_cell(self, e):
        pyperclip.copy(e.control.content.value)  # 复制到剪贴板
        self.info_snack_bar.content.value = "复制成功!"
        self.info_snack_bar.open = True
        self.page.update()

    # 导出密码点击事件
    def export_pwd_click(self, e):
        self.choose_export_dlg.open = True
        self.page.update()

    # 导出密码信息弹窗保存按钮
    def export_pwd_dlg_save(self, e):
        export_format = self.choose_export_dlg.content.controls[1].value
        if self.local_dir_path == "" or export_format == "":
            self.info_snack_bar.content.value = "请选择保存目录和导出格式!"
            self.info_snack_bar.open = True
            self.page.update()
            return
        else:
            pwd_list = db.query_password(db.conn, self.current_user)
            status = de.export_password(pwd_list, self.current_user, self.current_key, self.local_dir_path,
                                        export_format)
            if status == -1:
                self.info_snack_bar.content.value = "导出失败!"
                self.info_snack_bar.open = True
                self.page.update()
            else:
                self.page.close(self.choose_export_dlg)
                # 清除变量
                self.local_dir_path = ""
                self.choose_export_dlg.content.controls[0].controls[0].value = ""
                self.choose_export_dlg.content.controls[1].value = ""
                self.info_snack_bar.content.value = "导出成功!"
                self.info_snack_bar.open = True
                self.page.update()

    # 导出密码信息弹窗取消按钮
    def export_pwd_dlg_cancel(self, e):
        self.page.close(self.choose_export_dlg)
        # 清除变量
        self.local_dir_path = ""
        self.choose_export_dlg.content.controls[0].controls[0].value = ""
        self.choose_export_dlg.content.controls[1].value = ""

    # 目录选择结果
    def get_directory_result(self, e: ft.FilePickerResultEvent):
        if e.path is None:
            self.info_snack_bar.content.value = "请选择一个目录!"
            self.info_snack_bar.open = True
            self.page.update()
        else:
            self.choose_export_dlg.content.controls[0].controls[0].value = e.path
            self.local_dir_path = e.path
            self.page.update()

    # 导入密码点击事件
    def import_pwd_click(self, e):
        self.choose_import_dlg.open = True
        self.page.update()

    # 导入密码信息弹窗保存按钮
    def import_pwd_dlg_save(self, e):
        if self.local_file_path == "":
            self.info_snack_bar.content.value = "请选择一个文件!"
            self.info_snack_bar.open = True
            self.page.update()
            return
        else:
            # 拆分文件后缀
            file_suffix = self.local_file_path.split(".")[-1].upper()
            if file_suffix != "JSON" and file_suffix != "CSV" and file_suffix != "TXT":
                self.info_snack_bar.content.value = "文件格式错误!只支持JSON、CSV、TXT格式文件!"
                self.info_snack_bar.open = True
                self.page.update()
                return
            ok_count = 0
            error_count = 0
            pwd_list = de.import_password(self.current_user, self.local_file_path, file_suffix)
            if pwd_list == -1:
                self.info_snack_bar.content.value = "导入失败!"
                self.info_snack_bar.open = True
                self.page.update()
                return
            for pwd_info in pwd_list:
                flag = db.insert_password(db.conn, self.current_user, pwd_info['website_name'], pwd_info['website'],
                                          pwd_info['account'],
                                          de.data_encrypt(pwd_info['password'], de.pbkdf2(self.current_key),
                                                          pwd_info['encrypted_method']),
                                          pwd_info['encrypted_method'], pwd_info['note'])
                created_time = db.query_password_created_at(db.conn, self.current_user, pwd_info['website_name'],
                                                            pwd_info['account'])
                if flag == 1:
                    ok_count += 1
                    pwn_row = PwdRow(
                        cells=[
                            ft.DataCell(ft.Text(f"{pwd_info['website_name']}"), on_tap=self.copy_cell),
                            ft.DataCell(ft.Text(f"{pwd_info['account']}"), on_tap=self.copy_cell),
                            ft.DataCell(ft.Text(f"{pwd_info['password']}"), on_tap=self.copy_cell),
                            ft.DataCell(ft.Text(f"{pwd_info['website']}"), on_tap=self.copy_cell),
                            ft.DataCell(ft.Text(f"{pwd_info['note']}"), on_tap=self.copy_cell),
                            ft.DataCell(ft.Text(f"{created_time}"), on_tap=self.copy_cell),
                        ],
                        delete_pwd_row=self.delete_pwd_row
                    )
                    self.pwd_table.rows.append(pwn_row)
                else:
                    error_count += 1
            self.page.close(self.choose_import_dlg)
            # 清除变量
            self.local_file_path = ""
            self.choose_import_dlg.content.controls[0].controls[0].value = ""
            self.info_snack_bar.content.value = f"导入成功: {ok_count} 条!   导入失败: {error_count} 条!"
            self.info_snack_bar.open = True
            self.page.update()

    # 导入密码信息弹窗取消按钮
    def import_pwd_dlg_cancel(self, e):
        self.page.close(self.choose_import_dlg)
        # 清除变量
        self.local_file_path = ""
        self.choose_import_dlg.content.controls[0].controls[0].value = ""

    # 文件选择结果
    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files is None:
            self.info_snack_bar.content.value = "请选择一个文件!"
            self.page.overlay.append(self.info_snack_bar)
            self.info_snack_bar.open = True
            self.page.update()
        else:
            self.choose_import_dlg.content.controls[0].controls[0].value = e.files[0].path
            self.local_file_path = e.files[0].path
            self.page.update()


# 切换明暗主题
def change_theme(page):
    global BGCOLOR, THEME
    if page.theme_mode == ft.ThemeMode.LIGHT:
        BGCOLOR = "#050D18"
        THEME = ft.ThemeMode.DARK
        page.bgcolor = BGCOLOR
        page.theme_mode = THEME
    else:
        BGCOLOR = "#f0f0f0"
        THEME = ft.ThemeMode.LIGHT
        page.bgcolor = BGCOLOR
        page.theme_mode = THEME
    page.update()


# 主页面
def main_page(page, current_user, current_key):
    page.clean()
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER  # 垂直居中
    # page.window.min_height = 700
    # page.window.min_width = 1200
    page.window.width = 1200
    page.window.height = 700
    page.window.center()
    page.add(MainPage(current_user, current_key, page))
    page.update()
    page.on_disconnect = lambda: db.close_connection(db.conn)


# 注册界面
def Register_page(page):
    page.clean()
    page.window.min_width = 600
    page.window.min_height = 500
    page.window.width = 600
    page.window.height = 500
    # page.window.center()
    page.add(RegisterPage(page))
    page.update()
    page.on_disconnect = lambda: db.close_connection(db.conn)


# 登录页面
def main(page: ft.Page):
    page.clean()
    page.title = "密码管理器"
    page.window.bgcolor = ft.colors.TRANSPARENT
    page.bgcolor = BGCOLOR
    page.window.frameless = False
    page.window.min_width = 600
    page.window.min_height = 500
    page.window.width = 600
    page.window.height = 500
    page.update()
    page.auto_scroll = True
    page.scroll = "AUTO"
    page.window.center()
    page.theme_mode = THEME
    page.theme = ft.theme.Theme(color_scheme_seed='blue', font_family='source')
    page.fonts = {'source': 'https://www.unpkg.com/font-online/fonts/SourceHanSans/SourceHanSans-Normal.otf'}
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # 垂直居中
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 水平居中

    page.add(LoginPage(page))
    page.padding = 20
    page.update()
    page.on_disconnect = lambda: db.close_connection(db.conn)


# 如果捕捉到异常则关闭数据库连接
try:
    ft.app(target=main, assets_dir="asset")
except Exception:
    db.close_connection(db.conn)

# 打包命令
# flet pack main.py --add-data "asset;asset" --icon "D:\Desktop\PassWordManager\asset\logo.ico"
#  --product-name "PassManager"  --product-version "1.0" --file-version "1.0"
#  --file-description "A simple and safe password manager"
#  --copyright "By LiuChao"
