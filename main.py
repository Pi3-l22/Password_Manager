import flet as ft


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
    # page.update()

    # 登录按钮点击事件
    def btn_login_click(e):
        # TODO
        if username_box.value == "" and password_box.value == "":
            main_page(page)
        else:
            print("Wrong Username or Password!")
            page.overlay.append(w_pwd_dlg)
            w_pwd_dlg.open = True
            page.update()

    # 注册按钮点击事件
    def btn_register_click(e):
        pass

    # 主页
    def main_page(page):
        page.clean()
        # page.vertical_alignment = ft.MainAxisAlignment.CENTER  # 垂直居中
        page.window.height = 700
        page.window.min_height = 700
        page.window.width = 1000
        page.window.min_width = 1000
        page.window.center()
        page.update()

        # 添加密码按钮点击事件
        def btn_add_pwd_click(e):
            print("Add Password")
            pass

        # 搜索框提交事件
        def search_box_submit(e):
            print("Search")
            pass

        # 添加密码按钮
        btn_add_pwd = ft.IconButton(
            icon=ft.icons.ADD_CIRCLE,
            icon_size=70,
            tooltip="添加新的密码信息",
            on_click=btn_add_pwd_click,
        )

        # 搜索框
        search_box = ft.SearchBar(
            bar_hint_text="输入关键字搜索",
            on_submit=search_box_submit,
            width=600,
        )

        # 搜索提交按钮
        btn_search = ft.IconButton(
            icon=ft.icons.SEARCH,
            icon_size=70,
            tooltip="搜索",
            on_click=search_box_submit,
        )

        # 密码信息展示
        pwd_lists = ft.Column(
            height=400,
            width=650,
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("密码信息展示"),
            ]
        )

        page.add(ft.Column(
            [
                ft.Row(
                    [
                        btn_add_pwd,
                        search_box,
                        btn_search,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        pwd_lists,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=20
        ))

    # 登录事件错误弹窗
    w_pwd_dlg = ft.AlertDialog(
        title=ft.Text("用户名或密码错误", color="#043D79"),
        content=ft.Text("请检查你的用户名和密码是否正确!"),
    )
    e_lg_dlg = ft.AlertDialog(
        title=ft.Text(
            "Too Many Errors!\n\nPlease try again later in a few minutes!"),
    )
    d_dlg = ft.AlertDialog(
        title=ft.Text(
            "This user has been disabled!"
        )
    )
    p_dlg = ft.AlertDialog(
        title=ft.Text(
            "This user does not have permission!"
        )
    )

    # 注册事件错误弹窗
    # TODO

    # 主标题
    title = ft.Stack(
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
    logo_image = ft.Image(
        src="./asset/image/lock.png",
        width=100,
        height=140,
    )

    page.add(title)
    page.add(logo_image)

    # 用户名和密码输入框
    password_box = ft.TextField(
        label="Password",
        hint_text="请输入你的主密码",
        max_lines=1,
        width=350,
        height=55,
        password=True,
        can_reveal_password=True,
        keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
        shift_enter=True,
        on_submit=btn_login_click
    )
    username_box = ft.TextField(
        label="Username",
        hint_text="请输入你的用户名",
        max_lines=1,
        width=350,
        height=55,
        autofocus=True,
        shift_enter=True,
        on_submit=lambda e: password_box.focus(),
    )

    # 登录和注册按钮
    btn_login = ft.ElevatedButton(
        text="登入",
        width=150,
        height=50,
        animate_size=True,
        on_click=btn_login_click,
        icon=ft.icons.LOGIN,
    )
    btn_register = ft.ElevatedButton(
        text="注册",
        width=150,
        height=50,
        animate_size=True,
        on_click=btn_register_click,
        icon=ft.icons.PERSON_ADD_ALT,
    )

    # 登录框和按钮
    page.add(ft.Column(
        [
            ft.Row(
                [
                    # ft.Text("Username:"),
                    username_box
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    # ft.Text("Password:"),
                    password_box
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    btn_login,
                    btn_register,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=50,
            ),
        ],
        # 居中
        spacing=20,
    ))

    page.padding = 20  # 设置内边距
    page.update()


ft.app(target=main, assets_dir="asset")
