from loguru import logger as log
import datetime
import sys



class logger:
    def __init__(self):
        log.add(f"log/{datetime.datetime.now().strftime('%Y-%m-%d')}.log")
        log.add(sys.stderr, level="DEBUG")

    def debug(self, msg):
        log.debug(msg)
    def info(self, msg):
        log.info(msg)
    def warning(self, msg):
        log.warning(msg)
    def error(self, msg):
        log.error(msg)
    def debug(self, msg):
        log.debug(msg)
    def critical(self, msg):
        log.critical(msg)