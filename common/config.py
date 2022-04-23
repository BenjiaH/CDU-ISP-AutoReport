import os
import json
from common.logger import logger


class Config:
    def __init__(self, config_file=r"../config/config.json"):
        os.chdir(os.path.dirname(__file__))
        self._path = os.path.abspath(config_file)
        if not os.path.exists(self._path):
            logger.error(f"No such file:{self._path}")
            raise FileNotFoundError(f"No such file:{self._path}")
        self.config = {}
        self._json_read()

    @logger.catch
    def _json_read(self):
        with open(self._path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        logger.debug(f"Loaded [{self._path}]")

    @logger.catch
    def refresh(self):
        self._json_read()
        logger.debug(f"Refreshed [{self._path}]")


global_config = Config(r"../config/config.json")
