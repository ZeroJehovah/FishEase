import configparser
import os
from vo.RECT import RECT
from vo.FormInfo import FormInfo

CONFIG_FILE_CHARSET = "UTF-8"
CONFIG_DIR = "config"
APP_CONFIG_FILE = "app.ini"
FORM_CONFIG_FILE = "form.ini"
APP_CONFIG_TITLE = "title"
APP_CONFIG_CLASSNAME = "classname"
APP_CONFIG_SMALL_CLIENT_WIDTH = "small-client-width"
FORM_CONFIG_LEFT = "left"
FORM_CONFIG_TOP = "top"
FORM_CONFIG_RIGHT = "right"
FORM_CONFIG_BOTTOM = "bottom"
FORM_CONFIG_VOLUME = "volume"


class ConfigUtils:
    global_form_infos: list = []
    global_running_form_name: str = None
    global_form_small_rect: RECT = None
    global_form_volume: int = 0

    @staticmethod
    def init_global_form_infos():
        config = read_config(APP_CONFIG_FILE)
        for section in config.sections():
            if not get_config(config, section, APP_CONFIG_TITLE):
                continue
            form_info = FormInfo(section, get_config(config, section, APP_CONFIG_TITLE), get_config(config, section, APP_CONFIG_CLASSNAME), get_config(config, section, APP_CONFIG_SMALL_CLIENT_WIDTH))
            ConfigUtils.global_form_infos.append(form_info)

    @staticmethod
    def read_form_configs():
        config = read_config(FORM_CONFIG_FILE)
        ConfigUtils.global_form_small_rect = RECT(get_config(config, ConfigUtils.global_running_form_name, FORM_CONFIG_LEFT), get_config(config, ConfigUtils.global_running_form_name, FORM_CONFIG_TOP), get_config(config, ConfigUtils.global_running_form_name, FORM_CONFIG_RIGHT), get_config(config, ConfigUtils.global_running_form_name, FORM_CONFIG_BOTTOM))
        ConfigUtils.global_form_volume = get_config(config, ConfigUtils.global_running_form_name, FORM_CONFIG_VOLUME)
        ConfigUtils.global_form_volume = int(ConfigUtils.global_form_volume) if ConfigUtils.global_form_volume else 0

    @staticmethod
    def save_form_configs():
        config = configparser.ConfigParser()
        config[ConfigUtils.global_running_form_name] = {
            FORM_CONFIG_LEFT: str(ConfigUtils.global_form_small_rect.left),
            FORM_CONFIG_TOP: str(ConfigUtils.global_form_small_rect.top),
            FORM_CONFIG_RIGHT: str(ConfigUtils.global_form_small_rect.right),
            FORM_CONFIG_BOTTOM: str(ConfigUtils.global_form_small_rect.bottom),
            FORM_CONFIG_VOLUME: str(ConfigUtils.global_form_volume)
        }
        with open(FORM_CONFIG_FILE, 'w', encoding=CONFIG_FILE_CHARSET) as config_file:
            config.write(config_file)


def read_config(file_name: str):
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
    file_name = CONFIG_DIR + "/" + file_name
    if os.path.exists(file_name):  # 配置文件存在，读取配置
        print(f"read config from {file_name}")
        with open(file_name, 'r', encoding=CONFIG_FILE_CHARSET) as config_file:
            config.read_file(config_file)
        if len(config.sections()):
            return config
    if file_name == CONFIG_DIR + "/" + APP_CONFIG_FILE:  # 如果配置文件不存在，并且当前为程序配置，则初始化默认值
        print(f"init default configs for {file_name}")
        config["StarRail"] = {
            APP_CONFIG_TITLE: "崩坏：星穹铁道",
            APP_CONFIG_CLASSNAME: "UnityWndClass",
            APP_CONFIG_SMALL_CLIENT_WIDTH: "320"
        }
    # 写入配置文件
    print(f"create new config file: {file_name}")
    with open(file_name, 'w', encoding=CONFIG_FILE_CHARSET) as config_file:
        config.write(config_file)
    return config


def get_config(config: configparser, section: str, option: str):
    if config.has_section(section) and config.has_option(section, option):
        return config.get(section, option)
    return None
