from json import dumps
import win32con
from win32gui import *
from win32com import client

from utils.AudioUtils import reset_audio_session, change_to_original as change_audio_to_original, change_to_small as change_audio_to_small, init_running_audio_session
from utils.ConfigUtils import ConfigUtils, read_form_configs, save_form_configs
from vo.FormInfo import FormInfo
from vo.RECT import RECT

CHECK_FORM_EXISTS_TIMES = 5


class FormUtils:
    original_rect: RECT = None
    current_check_times: int = 0
    is_find_info_print: bool = False

    global_is_change_rect: bool = True
    global_running_form: int = 0
    global_running_form_info: FormInfo = None
    global_last_focus: int = None


def init_target_form():  # 检测当前是否有监测的窗口
    if not FormUtils.global_running_form:  # 如果没检测到目标窗口，则寻找
        return find_new_form_and_init()
    if IsWindow(FormUtils.global_running_form):
        FormUtils.current_check_times = 0
        return True
    # 连续5次检测目标窗口不存在，则取消监测
    FormUtils.current_check_times += 1
    if FormUtils.current_check_times > CHECK_FORM_EXISTS_TIMES:
        print(f"target form {FormUtils.global_running_form} is missing")
        FormUtils.current_check_times = 0
        FormUtils.global_running_form = 0
        FormUtils.global_running_form_info = None
        reset_audio_session()
        reset_notify_icon()
    return False


def change_to_original():  # 将目标窗口调整为原尺寸
    change_audio_to_original()
    if not FormUtils.global_running_form or not IsWindow(FormUtils.global_running_form):  # 如果窗口不存在，则不执行
        return
    if not FormUtils.global_is_change_rect:
        return
    if GetWindowPlacement(FormUtils.global_running_form)[1] == win32con.SW_SHOWMINIMIZED:
        ShowWindow(FormUtils.global_running_form, win32con.SW_RESTORE)
    if is_original():  # 当前已经处于原尺寸，无需执行
        return
    update_small_rect()
    if FormUtils.global_last_focus == FormUtils.global_running_form:
        SetWindowPos(FormUtils.global_running_form, win32con.HWND_NOTOPMOST, FormUtils.original_rect.left, FormUtils.original_rect.top, FormUtils.original_rect.width(), FormUtils.original_rect.height(), 0)
    else:
        SetWindowPos(FormUtils.global_running_form, FormUtils.global_last_focus, FormUtils.original_rect.left, FormUtils.original_rect.top, FormUtils.original_rect.width(), FormUtils.original_rect.height(), win32con.SWP_NOACTIVATE)
        change_focus_to_last_focus()
    print(f"change form {FormUtils.global_running_form} to original RECT")


def change_to_small():  # 将目标窗口缩小并置顶
    change_audio_to_small()
    if not FormUtils.global_running_form or not IsWindow(FormUtils.global_running_form):  # 如果窗口不存在，则不执行
        return
    if not FormUtils.global_running_form_info.enable_change_rect() or not FormUtils.global_is_change_rect:
        return
    if GetWindowPlacement(FormUtils.global_running_form)[1] == win32con.SW_SHOWMINIMIZED:
        return
    if not is_original():  # 当前已经处于缩小尺寸，无需执行
        return
    update_original_rect()
    SetWindowPos(FormUtils.global_running_form, win32con.HWND_TOPMOST, ConfigUtils.global_form_small_rect.left, ConfigUtils.global_form_small_rect.top, ConfigUtils.global_form_small_rect.width(), ConfigUtils.global_form_small_rect.height(), win32con.SWP_NOACTIVATE)
    print(f"change form {FormUtils.global_running_form} to small RECT")


def change_focus_to_last_focus():  # 将上一个焦点窗口重新设置为焦点
    if not FormUtils.global_last_focus or not IsWindow(FormUtils.global_last_focus):  # 如果窗口不存在，则不执行
        return
    last_focus_title = GetWindowText(FormUtils.global_last_focus)
    print("change focus to", last_focus_title)
    shell = client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    SetForegroundWindow(FormUtils.global_last_focus)


def get_window_rect(form: int):  # 对win32gui.GetWindowRect的简单封装
    left, top, right, bottom = GetWindowRect(form)
    return RECT(left, top, right, bottom)


def get_client_rect(form: int):  # 对win32gui.GetClientRect的简单封装
    left, top, right, bottom = GetClientRect(form)
    return RECT(left, top, right, bottom)


def find_new_form_and_init():  # 寻找待监测的窗口，找到后执行初始化
    for form_info in ConfigUtils.global_form_infos:
        if form_info.classname and len(form_info.classname):  # 如果配置了classname，则直接根据title和classname查找窗口
            if not FormUtils.is_find_info_print:
                print(f"find form by {form_info.title}(classname={form_info.classname})")
                FormUtils.is_find_info_print = True
            find_form = FindWindow(form_info.classname, form_info.title)
            if find_form:
                # print(f"found target form {find_form}: {form_info.title}(classname={form_info.classname})")
                return check_running_form(find_form, form_info)
        else:  # 如果未配置classname，则根据title找到所有的窗口，然后选择其中最大的一个
            if not FormUtils.is_find_info_print:
                print(f"find form by {form_info.title}")
                FormUtils.is_find_info_print = True
            find_forms = find_forms_by_title(form_info.title)
            if not len(find_forms):
                return False
            max_width = 0
            max_width_form = 0
            for find_form in find_forms:
                form_rect = get_window_rect(find_form)
                max_width, max_width_form = (form_rect.width(), find_form) if form_rect.width() > max_width else (max_width, max_width_form)
            if max_width_form:
                form_classname = GetClassName(max_width_form)
                print(f"found {len(find_forms)} forms named {form_info.title}, the largest form is {max_width_form}: {form_info.title}(classname={form_classname})")
                form_info.classname = form_classname
                return check_running_form(max_width_form, form_info)
    return False


def check_running_form(running_form: int, running_form_info: FormInfo):  # 检查找到的窗口是否符合要求，如果是，则初始化各项参数
    if not is_original(running_form, running_form_info.small_client_width if running_form_info.enable_change_rect() else 1):
        return False
    print(f"catch form {running_form} success: {running_form_info.title}(classname={running_form_info.classname})")
    FormUtils.is_find_info_print = False
    FormUtils.global_running_form = running_form
    FormUtils.global_running_form_info = running_form_info
    init_running_audio_session(running_form)
    set_notify_icon()
    init_form_configs()
    return True


def init_form_configs():  # 初始化窗口各项参数
    if not FormUtils.global_running_form_info.enable_change_rect():  # 如果未配置small_client_width，则禁用调整大小的功能
        return
    FormUtils.original_rect = get_window_rect(FormUtils.global_running_form)
    print(f"init target form's original RECT: {dumps(FormUtils.original_rect.__dict__)}")
    ConfigUtils.global_running_form_name = FormUtils.global_running_form_info.name
    read_form_configs()
    if ConfigUtils.global_form_small_rect.width() <= 0 or ConfigUtils.global_form_small_rect.height() <= 0:
        original_client_rect = get_client_rect(FormUtils.global_running_form)
        small_client_width = FormUtils.global_running_form_info.small_client_width
        small_client_height = int(small_client_width * original_client_rect.height() / original_client_rect.width())
        small_width = small_client_width + FormUtils.original_rect.width() - original_client_rect.width()
        small_height = small_client_height + FormUtils.original_rect.height() - original_client_rect.height()
        print(f"original client: width={original_client_rect.width()}, height={original_client_rect.height()}; small client: width={small_client_width}, height={small_client_height}")
        ConfigUtils.global_form_small_rect = RECT(FormUtils.original_rect.left, FormUtils.original_rect.top, FormUtils.original_rect.left + small_width, FormUtils.original_rect.top + small_height)
        print(f"init target form's small RECT: {dumps(ConfigUtils.global_form_small_rect.__dict__)}")
    else:
        print(f"load target form's small RECT from config file: {dumps(ConfigUtils.global_form_small_rect.__dict__)}")


def find_forms_by_title(title: str):  # 通过标题查找所有符合的窗口
    windows = []

    def callback(hwnd, _):
        if GetWindowText(hwnd) == title:
            windows.append(hwnd)
        return True

    EnumWindows(callback, None)
    return windows


def set_notify_icon():  # 设置通知栏图标
    from utils.NotifyIcon import set_nofify_icon
    set_nofify_icon(True, FormUtils.global_running_form_info.title, FormUtils.global_running_form_info.enable_change_rect())


def reset_notify_icon():  # 将通知栏图标初始化为未监测状态
    from utils.NotifyIcon import set_nofify_icon
    set_nofify_icon(False)


def update_small_rect():  # 更新缩小尺寸窗口的位置信息
    current_rect = get_window_rect(FormUtils.global_running_form)
    if ConfigUtils.global_form_small_rect != current_rect:  # 读取新的缩小尺寸并保存
        ConfigUtils.global_form_small_rect = current_rect
        print("update small RECT:", dumps(ConfigUtils.global_form_small_rect.__dict__))
        save_form_configs()


def update_original_rect():  # 更新原尺寸窗口的位置信息
    current_rect = get_window_rect(FormUtils.global_running_form)
    if FormUtils.original_rect != current_rect:  # 读取新的缩小尺寸并保存
        FormUtils.original_rect = current_rect
        print("update original RECT:", dumps(FormUtils.original_rect.__dict__))


def is_original(form: int = 0, small_client_width: int = 0):
    form = form if form else FormUtils.global_running_form
    small_client_width = small_client_width if small_client_width else FormUtils.global_running_form_info.small_client_width
    current_client_rect = get_client_rect(form)
    return current_client_rect.width() > small_client_width
