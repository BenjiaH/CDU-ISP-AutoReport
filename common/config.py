import os
import configparser
from common.logger import logger


class Config:
    def __init__(self, config_file=r"../config/config.ini"):
        os.chdir(os.path.dirname(__file__))
        self._path = config_file
        if not os.path.exists(self._path):
            logger.error("No such file:{file}".format(file=config_file))
            raise FileNotFoundError("No such file:{file}".format(file=config_file))
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')

    def refresh(self):
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw.read(self._path, encoding='utf-8-sig')

    def get(self, section, name):
        return self._config.get(section, name)

    def getRaw(self, section, name):
        return self._configRaw.get(section, name)


global_config = Config(r"../config/config.ini")
