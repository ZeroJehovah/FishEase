from os import path, getpid
from sys import exit
from psutil import NoSuchProcess, Process
import win32con
from win32gui import MessageBox

LOCK_FILE = ".lock"


def get_lock():
    last_pid = read_from_lock_file()
    if check_pid_exists(last_pid):
        MessageBox(0, "程序已经在运行了", "提示", win32con.MB_OK)
        exit(1)
    else:
        write_lock_file()


def read_from_lock_file():
    if path.exists(LOCK_FILE):
        with open(LOCK_FILE) as lock_file:
            last_pid = lock_file.read()
        if last_pid:
            try:
                return int(last_pid)
            except ValueError:
                return 0
    return 0


def write_lock_file():
    with open(LOCK_FILE, "w") as lock_file:
        lock_file.write(str(getpid()))


def check_pid_exists(pid: int):
    if pid <= 0:
        return False
    try:
        process = Process(pid)
        process_name = process.name()
        if process_name and process_name == Process(getpid()).name():
            return True
    except NoSuchProcess:
        return False
