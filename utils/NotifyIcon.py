from threading import Thread
from pystray import Menu, MenuItem, Icon
from PIL import Image

from utils.Timer import stop
from utils.FormUtils import FormUtils
from utils.ConfigUtils import ConfigUtils, save_form_configs

ICON_TITLE = "摸鱼小助手"
ICON_IMAGE = Image.open("resources/icon.ico")
DEFAULT_TITLE = "未发现目标窗口"
REPO_URL = "https://github.com/ZeroJehovah/FishEase"
VERSION = "1.0.5.0"


class NotifyInco:
    icon: Icon = None
    has_running_form: bool = False
    form_title: str = DEFAULT_TITLE
    enable_change_rect: bool = True


def init_notify_icon():  # 初始化通知栏图标
    menu_list = Menu(
        MenuItem(lambda item: NotifyInco.form_title, None, enabled=False),
        Menu.SEPARATOR,
        MenuItem('调节尺寸', change_size, enabled=lambda item: NotifyInco.has_running_form and NotifyInco.enable_change_rect, checked=lambda item: NotifyInco.has_running_form and FormUtils.global_is_change_rect and NotifyInco.enable_change_rect),
        MenuItem("前台音量", Menu(
            MenuItem('0%', lambda item: change_volume_fore(0), checked=lambda item: ConfigUtils.global_form_volume_fore == 0),
            MenuItem('10%', lambda item: change_volume_fore(10), checked=lambda item: ConfigUtils.global_form_volume_fore == 10),
            MenuItem('20%', lambda item: change_volume_fore(20), checked=lambda item: ConfigUtils.global_form_volume_fore == 20),
            MenuItem('30%', lambda item: change_volume_fore(30), checked=lambda item: ConfigUtils.global_form_volume_fore == 30),
            MenuItem('40%', lambda item: change_volume_fore(40), checked=lambda item: ConfigUtils.global_form_volume_fore == 40),
            MenuItem('50%', lambda item: change_volume_fore(50), checked=lambda item: ConfigUtils.global_form_volume_fore == 50),
            MenuItem('60%', lambda item: change_volume_fore(60), checked=lambda item: ConfigUtils.global_form_volume_fore == 60),
            MenuItem('70%', lambda item: change_volume_fore(70), checked=lambda item: ConfigUtils.global_form_volume_fore == 70),
            MenuItem('80%', lambda item: change_volume_fore(80), checked=lambda item: ConfigUtils.global_form_volume_fore == 80),
            MenuItem('90%', lambda item: change_volume_fore(80), checked=lambda item: ConfigUtils.global_form_volume_fore == 90),
            MenuItem('100%', lambda item: change_volume_fore(100), checked=lambda item: ConfigUtils.global_form_volume_fore == 100),
        ), enabled=lambda item: NotifyInco.has_running_form),
        MenuItem("后台音量", Menu(
            MenuItem('0%', lambda item: change_volume_back(0), checked=lambda item: ConfigUtils.global_form_volume_back == 0),
            MenuItem('10%', lambda item: change_volume_back(10), checked=lambda item: ConfigUtils.global_form_volume_back == 10),
            MenuItem('20%', lambda item: change_volume_back(20), checked=lambda item: ConfigUtils.global_form_volume_back == 20),
            MenuItem('30%', lambda item: change_volume_back(30), checked=lambda item: ConfigUtils.global_form_volume_back == 30),
            MenuItem('40%', lambda item: change_volume_back(40), checked=lambda item: ConfigUtils.global_form_volume_back == 40),
            MenuItem('50%', lambda item: change_volume_back(50), checked=lambda item: ConfigUtils.global_form_volume_back == 50),
            MenuItem('60%', lambda item: change_volume_back(60), checked=lambda item: ConfigUtils.global_form_volume_back == 60),
            MenuItem('70%', lambda item: change_volume_back(70), checked=lambda item: ConfigUtils.global_form_volume_back == 70),
            MenuItem('80%', lambda item: change_volume_back(80), checked=lambda item: ConfigUtils.global_form_volume_back == 80),
            MenuItem('90%', lambda item: change_volume_back(80), checked=lambda item: ConfigUtils.global_form_volume_back == 90),
            MenuItem('100%', lambda item: change_volume_back(100), checked=lambda item: ConfigUtils.global_form_volume_back == 100),
        ), enabled=lambda item: NotifyInco.has_running_form),
        Menu.SEPARATOR,
        # MenuItem('测试1', test),
        # MenuItem('测试2', test2),
        MenuItem(f"关于 v{VERSION}", about),
        MenuItem('退出', exit_app),
    )
    NotifyInco.icon = Icon(ICON_TITLE, ICON_IMAGE, ICON_TITLE, menu_list)
    Thread(target=NotifyInco.icon.run, daemon=True).start()


def set_nofify_icon(has_running_form: bool, form_title: str = None, enable_change_rect: bool = True):  # 设置通知栏内部分显示，可显示监测窗口的标题
    NotifyInco.has_running_form = has_running_form
    NotifyInco.form_title = form_title if form_title else DEFAULT_TITLE
    NotifyInco.enable_change_rect = enable_change_rect
    NotifyInco.icon.update_menu()


def change_size():  # “调节尺寸”的点击事件
    FormUtils.global_is_change_rect = not FormUtils.global_is_change_rect


def change_volume_fore(volume: int):  # “调节音量”的点击事件
    ConfigUtils.global_form_volume_fore = volume
    if ConfigUtils.global_form_volume_back > volume:
        ConfigUtils.global_form_volume_back = volume
    save_form_configs()


def change_volume_back(volume: int):  # “调节音量”的点击事件
    ConfigUtils.global_form_volume_back = volume
    if ConfigUtils.global_form_volume_fore < volume:
        ConfigUtils.global_form_volume_fore = volume
    save_form_configs()


def about():  # “关于”的点击事件
    import webbrowser
    webbrowser.open(REPO_URL)


def exit_app():  # “退出”的点击事件
    stop()
    NotifyInco.icon.stop()


# def test():
#     import win32gui
#     import win32con
#     win32gui.SetWindowPos(FormUtils.global_running_form, win32con.HWND_TOPMOST, ConfigUtils.global_form_small_rect.left, ConfigUtils.global_form_small_rect.top, ConfigUtils.global_form_small_rect.width(), ConfigUtils.global_form_small_rect.height(),
#                           win32con.SWP_NOACTIVATE)
#     win32gui.RedrawWindow(FormUtils.global_running_form, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
#     print("success")


# def test2():
#     import win32gui
#     import win32con
#     # win32gui.SetWindowPos(FormUtils.global_running_form, win32con.HWND_NOTOPMOST, FormUtils.original_rect.left, FormUtils.original_rect.top, FormUtils.original_rect.width(), FormUtils.original_rect.height(), 0)
#     win32gui.SetWindowPos(FormUtils.global_running_form, win32con.HWND_TOPMOST, ConfigUtils.global_form_small_rect.left + 100, ConfigUtils.global_form_small_rect.top + 100, ConfigUtils.global_form_small_rect.width(), ConfigUtils.global_form_small_rect.height(),
#                           win32con.SWP_NOACTIVATE)
#
#     win32gui.RedrawWindow(FormUtils.global_running_form, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
#     print("success")


def get_verison():
    return VERSION
