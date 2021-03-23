import os
import sys

from loguru import logger


class Logger:
    def __init__(self, log_file: str, debug_file: str):
        self._log_fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} [<level>{level:<5}</level>]{file}.{line}: {message}"
        self._debug_fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} [<level>{level:}</level>] {name}:{function}:{line}: {message}"
        os.chdir(os.path.dirname(__file__))
        logger.remove()
        logger.add(sink=log_file, filter=self.run_filter, format=self._log_fmt)
        logger.add(sink=sys.stderr, filter=self.run_filter, format=self._log_fmt)
        logger.add(sink=debug_file, filter=self.debug_filter, format=self._debug_fmt)
        logger.info("Logger started.")
        self.logger = logger

    @staticmethod
    def debug_filter(record):
        return record["level"].name == "DEBUG"

    @staticmethod
    def run_filter(record):
        return record["level"].name == "INFO" or record["level"].name == "ERROR"

    @staticmethod
    def log_version(stage: str, version=""):
        commit_id = ""
        if os.path.exists("../.git"):
            commit_id = (os.popen("git rev-parse --short HEAD").read()).replace("\n", "")
            version += "."
        info = version + commit_id + "(" + stage + ")"
        logger.info("Version:{version}".format(version=info))


handlers = Logger("../log.log", "../debug.log")
logger = handlers.logger
log_version = handlers.log_version
