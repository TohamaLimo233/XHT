import json
import os
import APP.LogMaker as LogMaker

log = LogMaker.logger()

DEFAULT_CONFIG = {
    "edge_height": 4,
    "horizontal_edge_margin": 4,
    "drag_threshold": 8,
    "windowpos": "R",
    "auto_hide_apps": ["PowerPoint ", "WPS Presentation Slide "]    
}
def check():
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
    config_file = os.path.join(config_dir, "appsettings.json")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        log.warn("配置文件不存在，已创建默认配置文件")
        return
    else:
        return    

def load_config():
    check()
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
    config_file = os.path.join(config_dir, "appsettings.json")
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        log.error(f"加载配置文件失败: {e}")
        return {}