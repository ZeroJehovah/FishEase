import os
import threading
import pkg_resources
import sys
import pystray
from PIL import Image

from utils.Timer import Timer
from utils.FormUtils import FormUtils
from utils.ConfigUtils import ConfigUtils

ICON_TITLE = "摸鱼小助手"
ICON_IMAGE = Image.open(os.path.join(getattr(sys, "_MEIPASS", ""), "resources/icon.ico"))
DEFAULT_TITLE = "未运行"
REPO_URL = "https://github.com/ZeroJehovah/FishEase"
VERSION = "v0.1"


class NotifyInco:
    icon: pystray.Icon = None
    has_running_form: bool = False
    form_title: str = DEFAULT_TITLE
    enable_change_size: bool = True

    @staticmethod
    def init():  # 初始化通知栏图标
        menu_list = pystray.Menu(
            pystray.MenuItem(lambda item: NotifyInco.form_title, None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('调节尺寸', change_size, enabled=lambda item: NotifyInco.has_running_form and NotifyInco.enable_change_size, checked=lambda item: NotifyInco.has_running_form and FormUtils.global_is_change_rect and NotifyInco.enable_change_size),
            pystray.MenuItem("调节音量", pystray.Menu(
                pystray.MenuItem('0(静音)', lambda item: change_volume(0), checked=lambda item: ConfigUtils.global_form_volume == 0),
                pystray.MenuItem('10%', lambda item: change_volume(10), checked=lambda item: ConfigUtils.global_form_volume == 10),
                pystray.MenuItem('20%', lambda item: change_volume(20), checked=lambda item: ConfigUtils.global_form_volume == 20),
                pystray.MenuItem('30%', lambda item: change_volume(30), checked=lambda item: ConfigUtils.global_form_volume == 30),
                pystray.MenuItem('40%', lambda item: change_volume(40), checked=lambda item: ConfigUtils.global_form_volume == 40),
                pystray.MenuItem('50%', lambda item: change_volume(50), checked=lambda item: ConfigUtils.global_form_volume == 50),
                pystray.MenuItem('60%', lambda item: change_volume(60), checked=lambda item: ConfigUtils.global_form_volume == 60),
                pystray.MenuItem('70%', lambda item: change_volume(70), checked=lambda item: ConfigUtils.global_form_volume == 70),
                pystray.MenuItem('80%', lambda item: change_volume(80), checked=lambda item: ConfigUtils.global_form_volume == 80),
                pystray.MenuItem('90%', lambda item: change_volume(80), checked=lambda item: ConfigUtils.global_form_volume == 90),
                pystray.MenuItem('100%(不调整)', lambda item: change_volume(100), checked=lambda item: ConfigUtils.global_form_volume == 100),
            ), enabled=lambda item: NotifyInco.has_running_form),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(f"关于 {VERSION}", about),
            pystray.MenuItem('退出', exit_app),
        )
        NotifyInco.icon = pystray.Icon(ICON_TITLE, ICON_IMAGE, ICON_TITLE, menu_list)
        threading.Thread(target=NotifyInco.icon.run, daemon=True).start()

    @staticmethod
    def set_nofify_icon(has_running_form: bool, form_title: str = None, enable_change_size: bool = True):  # 设置通知栏内部分显示，可显示监测窗口的标题
        NotifyInco.has_running_form = has_running_form
        NotifyInco.form_title = form_title if form_title else DEFAULT_TITLE
        NotifyInco.enable_change_size = enable_change_size
        NotifyInco.icon.update_menu()


def change_size():  # “调节尺寸”的点击事件
    FormUtils.global_is_change_rect = not FormUtils.global_is_change_rect


def change_volume(volume: int):  # “调节音量”的点击事件
    ConfigUtils.global_form_volume = volume
    ConfigUtils.save_form_configs()


def about():  # “关于”的点击事件
    import webbrowser
    webbrowser.open(REPO_URL)


def exit_app():  # “退出”的点击事件
    Timer.stop()
    NotifyInco.icon.stop()
