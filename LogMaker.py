import logging
import coloredlogs
import sys


class logger:
    def __init__(self):
        log_colors = {
            "DEBUG": "blue",
            "INFO": "white",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
        log_field_styles = {
            "asctime": {"color": "green"},
            "levelname": {"color": "white"}
        }
        coloredlogs.install(
            isatty=True, 
            stream=sys.stdout, 
            field_styles=log_field_styles, 
            fmt="[%(asctime)s] [%(levelname)s] %(message)s", 
            colors=log_colors,
            level=logging.INFO
        )
    
    def debug(self, msg):
        logging.debug(msg)
    def info(self, msg):
        logging.info(msg)
    def warn(self, msg):
        logging.info(msg)
    def error(self, msg):
        logging.error(msg)
    def debug(self, msg):
        logging.debug(msg)
    def cirical(self, msg):
        logging.critical(msg)