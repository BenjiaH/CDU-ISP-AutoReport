import os
import csv

from common.logger import logger
from common.config import global_config


class Account(object):
    @logger.catch
    def __init__(self, csv_file="../config/account.csv"):
        if global_config.getRaw('config', 'multiple_enable') == "off":
            logger.debug("Multiple mode disabled")
            return

        os.chdir(os.path.dirname(__file__))
        self._path = os.path.abspath(csv_file)
        if not os.path.exists(self._path):
            logger.error(f"No such file:{self._path}")
            raise FileNotFoundError(f"No such file:{self._path}")
        self._csv_file = open(self._path, encoding='utf-8')
        self._account = csv.reader(self._csv_file)
        self._row = sum(1 for line in open(self._path, encoding='utf-8')) - 1
        self._col = len(next(self._account))
        self._all_info = self.get_info()
        logger.debug(f"Loaded:{self._path}")

    @logger.catch
    def refresh(self):
        self._csv_file = open(self._path, encoding='utf-8')
        self._account = csv.reader(self._csv_file)
        self._row = sum(1 for line in open(self._path, encoding='utf-8')) - 1
        self._col = len(next(self._account))
        self._all_info = self.get_info()
        logger.debug(f"Refreshed:{self._path}")

    @logger.catch
    def get_info(self):
        ret = [[] for i in range(self._col)]
        for item in self._account:
            for i in range(self._col):
                ret[i].append(item[i])
        # # need not to remove first row, don't know why....
        # for i in range(self._row + 1):
        #     ret[i][:] = ret[i][1:]
        return ret

    @property
    def studentID(self):
        return self._all_info[0]

    @property
    def password(self):
        return self._all_info[1]

    @property
    def wechat_push(self):
        return self._all_info[2]

    @property
    def email_push(self):
        return self._all_info[3]

    @property
    def sendkey(self):
        return self._all_info[4]

    @property
    def userid(self):
        return self._all_info[5]

    @property
    def email(self):
        return self._all_info[6]

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col


global_account = Account("../config/account.csv")
