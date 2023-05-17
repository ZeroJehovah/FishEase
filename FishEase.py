from utils.Timer import Timer
from utils.ConfigUtils import ConfigUtils
from utils.NotifyIcon import NotifyInco

if __name__ == '__main__':
    NotifyInco.init()
    ConfigUtils.init_global_form_infos()
    Timer().main_loop()
