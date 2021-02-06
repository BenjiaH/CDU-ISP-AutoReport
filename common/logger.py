import os
import logging
import logging.handlers

LOG_FILENAME = __file__[:-16] + 'log.log'
logger = logging.getLogger()


def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)5s] %(filename)s[line:%(lineno)d]: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


set_logger()
logger.info("Logger started.")
version = (os.popen('git rev-parse --short HEAD').read()).replace("\n", "")
logger.info("Version:{version}".format(version=version))
