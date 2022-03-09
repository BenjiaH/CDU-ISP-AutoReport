import os
import sys

from loguru import logger


class Logger:
    def __init__(self, log_file: str):
        os.chdir(os.path.dirname(__file__))
        self._config_path = os.path.abspath(r"../config/config.ini")
        self._log_fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} [<level>{level:<5}</level>] {file}.{line}: {message}"
        self._debug_fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} [<level>{level:<5}</level>] {name}:{function}:{line}: {message}"
        self._logger_conf(log_file)
        self.logger = logger

    def _logger_conf(self, log_file):
        self._get_level()
        logger.remove()
        logger.add(sink=sys.stderr, format=self._log_fmt, level="INFO")
        if self._level == "INFO":
            logger.add(sink=log_file, format=self._log_fmt, rotation="1 MB", level=self._level)
        else:
            logger.add(sink=log_file, format=self._debug_fmt, rotation="1 MB", level=self._level)
        logger.info("The logger is started".center(50, '-'))
        if self._level == "DEBUG":
            logger.debug("The debug mode is enabled.")

    def _get_level(self):
        level_raw = "level = INFO"
        with open(self._config_path, "r", encoding="UTF-8") as f:
            lines = f.readlines()
            for i in lines:
                if "level" in i and ";" != i[0]:
                    level_raw = i
        if "DEBUG" in level_raw:
            self._level = "DEBUG"
        else:
            self._level = "INFO"

    @staticmethod
    @logger.catch
    def log_version(stage: str, version=""):
        commit_id = ""
        if os.path.exists("../.git"):
            logger.debug(f'Founded:{os.path.abspath("../.git")}.')
            commit_id = (os.popen("git rev-parse --short HEAD").read()).replace("\n", "")
            version += "."
        info = version + commit_id + "(" + stage + ")"
        logger.info(f"Version:{info}")


handlers = Logger("../log/log.log")
logger = handlers.logger
log_version = handlers.log_version
