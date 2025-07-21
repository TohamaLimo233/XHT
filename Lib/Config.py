import json
import os
import Lib.LogMaker as LogMaker

log = LogMaker.logger()

DEFAULT_CONFIG = {}
def check():
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config"))
        with open("config/appsettings.json", "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        log.warn("配置文件不存在，已创建默认配置文件")
        return
    else:
        return
    

def load_config():
    check()
    with open("config/appsettings.json", "r") as f:
        config = json.load(f)
    return config