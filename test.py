import flet as ft
import pyperclip
from gvcode import VFCode
import data_encrypto as de
import database_op as db


# 登录页面
class LoginPage(ft.Column):
    def __init__(self):
        super().__init__()
        # 主标题
        self.title = ft.Stack(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "密码管理器",
                            ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                letter_spacing=25,
                                foreground=ft.Paint(
                                    color="#0C6CC9",
                                    stroke_width=6,
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
                                size=40,
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
        self.logo_image = ft.Image(
            src="./asset/image/lock.png",
            width=100,
            height=100,
        )

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
            title=ft.Text("用户名或密码错误", color="#043D79"),
            content=ft.Text("请检查你的用户名和密码是否正确!"),
        )
        self.w_no_user_dlg = ft.AlertDialog(
            title=ft.Text("用户名或密码为空", color="#043D79"),
            content=ft.Text("请输入你的用户名和密码!"),
        )

        # 注册事件错误弹窗
        self.w_register_dlg = ft.AlertDialog(
            title=ft.Text("注册失败", color="#043D79"),
            content=ft.Text("请重新输入用户名和密码！"),
        )
        self.w_vf_code_dlg = ft.AlertDialog(
            title=ft.Text("验证码错误", color="#043D79"),
            content=ft.Text("请重新输入验证码！"),
        )

        # 注册验证码弹窗
        self.vf_code_dlg = ft.AlertDialog(
            title=ft.Text("验证码", color="#043D79"),
            content=ft.Row(
                [
                    ft.TextField(
                        label="验证码",
                        hint_text="请输入验证码",
                        max_lines=1,
                        width=100,
                        height=40,
                    ),
                    ft.Image(
                        src="register_code.png",
                        width=100,
                        height=40,
                    ),
                ]
            ),
            actions=[
                ft.OutlinedButton(
                    text="确定",
                    on_click=self.vf_code_dlg_confirm
                ),
                ft.OutlinedButton(
                    text="取消",
                    on_click=self.vf_code_dlg_cancel
                ),
            ]
        )
        # 注册成功弹窗
        self.w_register_success_dlg = ft.AlertDialog(
            title=ft.Text("注册成功", color="#043D79"),
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
                    self.logo_image,
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
            self.page.overlay.append(self.w_no_user_dlg)
            self.w_no_user_dlg.open = True
            self.page.update()
        else:
            # 数据库操作
            password = db.query_user(db.conn, self.username_box.value)
            if password is not None:
                if password == de.sha3_256(self.password_box.value):
                    main_page(self.page)
                else:
                    self.page.overlay.append(self.w_pwd_dlg)
                    self.w_pwd_dlg.open = True
                    self.page.update()
            else:
                self.page.overlay.append(self.w_pwd_dlg)
                self.w_pwd_dlg.open = True
                self.page.update()

    # 注册按钮点击事件
    def btn_register_click(self, e):
        if self.username_box.value == "" or self.password_box.value == "":
            self.page.overlay.append(self.w_no_user_dlg)
            self.w_no_user_dlg.open = True
            self.page.update()
        else:
            # 数据库操作
            password = db.query_user(db.conn, self.username_box.value)
            if password is None:
                # 生成验证码
                vc = VFCode()
                vc.generate_mix(4)
                vc.save("register_code.png")
                self.code = vc.code
                # 验证码弹窗
                self.page.overlay.append(self.vf_code_dlg)
                self.vf_code_dlg.open = True
                self.page.update()
            else:
                self.page.overlay.append(self.w_register_dlg)
                self.w_register_dlg = True
                self.page.update()

    # 注册验证码弹窗确定按钮
    def vf_code_dlg_confirm(self, e):
        # 验证验证码
        if self.vf_code_dlg.content.controls[0].value == self.code:
            # 数据库操作
            if db.insert_user(db.conn, self.username_box.value, de.sha3_256(self.password_box.value)) == 1:
                self.page.close(self.vf_code_dlg)
                self.page.overlay.append(self.w_register_success_dlg)
                self.w_register_success_dlg.open = True
                self.page.update()
            else:
                self.page.close(self.vf_code_dlg)
                self.page.overlay.append(self.w_register_dlg)
                self.w_register_dlg = True
                self.page.update()
        else:
            self.page.close(self.vf_code_dlg)
            self.page.overlay.append(self.w_vf_code_dlg)
            self.w_vf_code_dlg.open = True
            self.page.update()

    # 注册验证码弹窗取消按钮
    def vf_code_dlg_cancel(self, e):
        self.page.close(self.vf_code_dlg)
        self.page.update()


# 添加密码信息弹窗对象
class AddPwdDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.title = ft.Text("添加新密码信息", color="#043D79")
        self.content = ft.Column(
            [
                ft.TextField(
                    label="名称",
                    hint_text="请输入名称",
                    max_lines=1,
                    width=500,
                    height=55,
                ),
                ft.TextField(
                    label="账号",
                    hint_text="请输入账号",
                    max_lines=1,
                    width=500,
                    height=55,
                ),
                ft.TextField(
                    label="密码",
                    hint_text="请输入密码",
                    max_lines=1,
                    width=500,
                    height=55,
                ),
                ft.TextField(
                    label="网址",
                    hint_text="请输入网址",
                    max_lines=1,
                    width=500,
                    height=55,
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
                        ft.dropdown.Option("AES-256"),
                        ft.dropdown.Option("ChaCha20"),
                        ft.dropdown.Option("XChaCha20"),
                    ],
                ),
            ],
            width=500,
            height=500,
            spacing=25,
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.actions = [
            ft.OutlinedButton(
                text="保存",
                on_click=self.add_pwn_dlg_save
            ),
            ft.OutlinedButton(
                text="取消",
                on_click=self.add_pwn_dlg_cancel
            ),
        ]

    # 添加密码信息弹窗取消按钮
    def add_pwn_dlg_cancel(self, e):
        self.page.close(self)

    # 添加密码信息弹窗保存按钮
    def add_pwn_dlg_save(self, e):
        self.page.close(self)
        self.update()
        # 获取输入框信息
        name = self.content.controls[0].value
        account = self.content.controls[1].value
        password = self.content.controls[2].value
        url = self.content.controls[3].value
        remark = self.content.controls[4].value
        encrypto = self.content.controls[5].value

        # TODO 数据库操作
        print(name, account, password, url, remark, encrypto)


# 密码信息
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
            title=ft.Text("删除密码信息", color="#043D79"),
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


# 主页面
class MainPage(ft.Column):
    def __init__(self):
        super().__init__()

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

        # 密码信息表
        self.pwd_table = ft.DataTable(
            width=1100,
            bgcolor='#44C0DDEE',
            border_radius=20,
            heading_text_style=ft.TextStyle(color="#043D79", weight=ft.FontWeight.BOLD, size=16),
            column_spacing=10,
            columns=[
                ft.DataColumn(ft.Text("名称")),
                ft.DataColumn(ft.Text("账号")),
                ft.DataColumn(ft.Text("密码")),
                ft.DataColumn(ft.Text("网址")),
                ft.DataColumn(ft.Text("备注")),
                ft.DataColumn(ft.Text("日期")),
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
                    self.btn_add_pwd,
                    self.search_box,
                    self.btn_search,
                    self.btn_import,
                    self.btn_export,
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
        for i in range(10):
            pwd_info = PwdRow(
                cells=[
                    ft.DataCell(ft.Text("John John John"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text("Smith Smith Smith"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text("1234567890123456789"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text("1234567890123456789"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text("1234567890123456789"), on_tap=self.copy_cell),
                    ft.DataCell(ft.Text("1234567890123456789"), on_tap=self.copy_cell),
                ],
                delete_pwd_row=self.delete_pwd_row
            )
            self.pwd_table.rows.append(pwd_info)

    # 添加密码按钮点击事件
    def btn_add_pwd_click(self, e):
        # 创建添加密码信息弹窗对象
        add_pwd_dlg = AddPwdDialog()
        self.page.overlay.append(add_pwd_dlg)
        add_pwd_dlg.open = True
        self.page.update()

    # 搜索框提交事件
    def search_box_submit(self, e):
        pass

    # 删除密码表格信息
    def delete_pwd_row(self, pwd_row):
        self.pwd_table.rows.remove(pwd_row)
        self.update()

    # 复制单元格内容
    def copy_cell(self, e):
        pyperclip.copy(e.control.content.value)  # 复制到剪贴板
        copy_snack_bar = ft.SnackBar(ft.Text("复制成功!"), duration=2000)
        self.page.overlay.append(copy_snack_bar)
        copy_snack_bar.open = True
        self.page.update()

    # 导入密码信息
    def import_pwd_click(self, e):
        pass

    # 导出密码信息
    def export_pwd_click(self, e):
        pass


# 主页面
def main_page(page):
    page.clean()
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER  # 垂直居中
    page.window.height = 700
    page.window.min_height = 700
    page.window.width = 1200
    page.window.min_width = 1200
    page.window.center()
    page.add(MainPage())
    page.update()
    page.on_disconnect = lambda: db.close_connection(db.conn)


# 登录页面
def main(page: ft.Page):
    page.title = "密码管理器"
    page.window.bgcolor = ft.colors.TRANSPARENT
    page.bgcolor = "#f0f0f0"
    page.window.frameless = False
    page.window.width = 600
    page.window.height = 500
    page.window.min_width = 600
    page.window.min_height = 500
    page.auto_scroll = True
    page.scroll = "AUTO"
    page.window.center()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.theme.Theme(color_scheme_seed='blue', font_family='Alibaba')
    page.fonts = {'Alibaba': '/fonts/AlibabaPuHuiTi.ttf'}
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # 垂直居中
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 水平居中

    page.add(LoginPage())
    page.padding = 20
    page.update()
    page.on_disconnect = lambda: db.close_connection(db.conn)


ft.app(target=main, assets_dir="asset")
