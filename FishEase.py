from utils.ConfigUtils import init_app_configs
from utils.LockUtils import get_lock
from utils.NotifyIcon import init_notify_icon
from utils.Timer import main_loop

if __name__ == '__main__':
    get_lock()
    init_notify_icon()
    init_app_configs()
    main_loop()
