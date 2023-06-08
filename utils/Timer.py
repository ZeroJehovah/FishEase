from time import sleep
from keyboard import is_pressed

from utils.FormUtils import *

MAIN_LOOP_DELAY = 0.1
SYS_FORM_TITLE = ["任务切换", "任务视图", "搜索"]


class Timer:
    alt_moving: bool = False
    loop: bool = True


def main_loop():  # 程序主循环
    while Timer.loop:
        # print(f"loop: {Timer.loop}")
        main_loop_action()
        sleep(MAIN_LOOP_DELAY)
    FormUtils.global_is_change_rect = True
    change_to_original(100)


def stop():  # 退出主循环
    Timer.loop = False


def main_loop_action():  # 程序主要逻辑，循环监测目标窗口是否存在，如存在，监测其是否获取焦点
    if not init_target_form():
        return
    current_focus = GetForegroundWindow()
    current_focus_title = GetWindowText(current_focus)
    # print("current focus title:", current_focus_title)
    if not current_focus_title or current_focus_title in SYS_FORM_TITLE:  # 当前焦点是系统组件，则视为未改变焦点状态
        current_focus = FormUtils.global_last_focus
    elif FormUtils.global_running_form_info.enable_change_rect() and FormUtils.global_is_change_rect:
        is_alt_pressed = is_pressed('alt')
        if current_focus == FormUtils.global_running_form and is_alt_pressed:
            Timer.alt_moving = True
            current_focus = FormUtils.global_last_focus
        elif current_focus == FormUtils.global_running_form and not is_alt_pressed and Timer.alt_moving:
            Timer.alt_moving = False
            change_focus_to_last_focus()
            current_focus = FormUtils.global_last_focus
        elif not is_alt_pressed:
            Timer.alt_moving = False
    if current_focus == FormUtils.global_last_focus:
        # print("focus is not change")
        pass
    else:
        print(f"change focus to: {current_focus_title}")
        FormUtils.global_last_focus = current_focus
    if current_focus == FormUtils.global_running_form:  # 目标窗口为缩小尺寸时获取焦点，则改变为原尺寸
        change_to_original()
    else:  # 目标窗口为原尺寸时失去焦点，则改变为缩小尺寸
        change_to_small()
