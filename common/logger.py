import os
import sys

from loguru import logger


class Logger:
    def __init__(self, log_file: str, debug_file=""):
        os.chdir(os.path.dirname(__file__))
        self._log_fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} [<level>{level:<5}</level>] {file}.{line}: {message}"
        self._debug_fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} [<level>{level:}</level>] {name}:{function}:{line}: {message}"
        self._config_path = os.path.abspath(r"../config/config.ini")
        logger.remove()
        logger.add(sink=log_file, filter=self.log_filter, format=self._log_fmt)
        logger.add(sink=sys.stderr, filter=self.log_filter, format=self._log_fmt)
        logger.info("The logger is started.")
        if self._is_debug():
            logger.add(sink=debug_file, filter=self.debug_filter, format=self._debug_fmt, rotation="1 MB")
            logger.debug("The logger is started.")
            logger.debug("The debug mode is enabled.")
        self.logger = logger

    def _is_debug(self):
        try:
            with open(self._config_path, "r", encoding="UTF-8") as f:
                if "*DEBUG = ON*" in f.read():
                    return True
                else:
                    return False
        except Exception as e:
            logger.error("{e}".format(e=e))
            return False

    @staticmethod
    def debug_filter(record):
        return record["level"].name == "DEBUG"

    @staticmethod
    def log_filter(record):
        return record["level"].name == "INFO" or record["level"].name == "ERROR"

    @staticmethod
    @logger.catch
    def log_version(stage: str, version=""):
        commit_id = ""
        if os.path.exists("../.git"):
            logger.debug("Founded:{git_path}.".format(git_path=os.path.abspath("../.git")))
            commit_id = (os.popen("git rev-parse --short HEAD").read()).replace("\n", "")
            version += "."
        info = version + commit_id + "(" + stage + ")"
        logger.info("Version:{version}".format(version=info))
        logger.debug("Version:{version}".format(version=info))


handlers = Logger("../log/log/log.log", "../log/debug/debug.log")
logger = handlers.logger
log_version = handlers.log_version
