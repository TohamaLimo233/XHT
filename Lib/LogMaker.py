from loguru import logger as log
import datetime
import sys



class logger:
    def __init__(self):
        # 移除默认的日志处理器，避免重复记录
        log.remove()
        # 添加文件日志处理器
        log.add(f"log/{datetime.datetime.now().strftime('%Y-%m-%d')}.log", 
                format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
                level="DEBUG")
        # 添加控制台日志处理器，保留颜色显示
        log.add(sys.stderr, 
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
                level="DEBUG",
                colorize=True)

    def info(self, msg):
        log.info(msg)
    def warn(self, msg):
        log.warn(msg)
    def error(self, msg):
        log.error(msg)
    def critical(self, msg):
        log.critical(msg)
