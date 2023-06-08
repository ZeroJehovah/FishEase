from threading import Thread
from time import sleep
from psutil import Process
from win32process import GetWindowThreadProcessId
from pycaw.utils import AudioSession, AudioUtilities

from utils.ConfigUtils import ConfigUtils

EASING_TIME: float = 0.01
EASING_STEPS: float = 2


class AudioUtils:
    running_process_name: str = None
    running_audio_session: AudioSession = None
    current_volume: int = 100
    target_volume: int = 100
    easing_thread = None


def init_running_audio_session(running_form: int = None):  # 初始化监测窗口的音频进程
    if running_form:
        _, pid = GetWindowThreadProcessId(running_form)
        if pid:
            process = Process(pid)
            process_name = process.name()
            if process_name:
                print(f"current form {running_form}'s pid is {pid}, proccess name is {process_name}")
                AudioUtils.running_process_name = process_name
                find_audio_session()
            else:
                print(f"current form {running_form}'s pid is {pid}, but unable to find it's process_name")
        else:
            print("unable to find current form {running_form}'s pid")
    else:
        reset_audio_session()


def change_to_original(volume: int):  # 把音量调整到设置的前台音量
    volume = volume if volume else ConfigUtils.global_form_volume_fore
    set_volume(volume)


def change_to_small():  # 把音量调整小，具体值在右键菜单里设置
    set_volume(ConfigUtils.global_form_volume_back)


def reset_audio_session():
    AudioUtils.current_volume = 100
    AudioUtils.target_volume = 100
    AudioUtils.running_audio_session = None


def find_audio_session():  # 根据进程名查找进程对象
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == AudioUtils.running_process_name:
            AudioUtils.running_audio_session = session
            print(f"found {AudioUtils.running_process_name}'s audio session")
            return


def set_volume(volume: int):  # 设置音量，有淡入淡出效果
    if AudioUtils.current_volume == volume:
        return
    if not AudioUtils.running_audio_session:
        find_audio_session()
        if not AudioUtils.running_audio_session:
            return
    AudioUtils.target_volume = volume
    if AudioUtils.easing_thread and AudioUtils.easing_thread.is_alive():
        return
    # AudioUtils.easing_thread.clear()
    AudioUtils.easing_thread = Thread(target=easing)
    AudioUtils.easing_thread.start()
    # AudioUtils.easing_thread.join()


def easing():  # 设置音量的循环
    # print("change volume")
    while AudioUtils.current_volume >= AudioUtils.target_volume + EASING_STEPS or AudioUtils.current_volume <= AudioUtils.target_volume - EASING_STEPS:
        if AudioUtils.current_volume > AudioUtils.target_volume:
            AudioUtils.current_volume -= EASING_STEPS
        elif AudioUtils.current_volume < AudioUtils.target_volume:
            AudioUtils.current_volume += EASING_STEPS
        AudioUtils.running_audio_session.SimpleAudioVolume.SetMasterVolume(AudioUtils.current_volume / 100, None)
        sleep(EASING_TIME)
    print(f"change volume to: {AudioUtils.current_volume}")
