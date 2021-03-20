import os
import logging
import logging.handlers

os.chdir(os.path.dirname(__file__))
LOG_FILENAME = os.path.abspath(r"../log.log")
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


def log_version(stage: str, version=""):
    commit_id = ""
    if os.path.exists("../.git"):
        commit_id = (os.popen("git rev-parse --short HEAD").read()).replace("\n", "")
        commit_id += "."
    version += "."
    info = version + commit_id + stage
    logger.info("Version:{version}.".format(version=info))


set_logger()
logger.info("Logger started.")
