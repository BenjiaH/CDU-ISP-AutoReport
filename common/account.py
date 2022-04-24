import os
import csv

from common.logger import logger
from common.config import global_config as gc


class Account:
    @logger.catch
    def __init__(self, csv_file="../config/account.csv"):
        example = os.path.abspath("../config/account_example.csv")
        os.chdir(os.path.dirname(__file__))
        self._path = os.path.abspath(csv_file)
        if not os.path.exists(self._path):
            logger.error(f"No such file [{self._path}]")
            if os.path.exists(example):
                logger.error(f"Please rename [{example}] to [{self._path}]")
            raise FileNotFoundError(f"No such file [{self._path}]")
        self._csv_file = None
        self._raw = []
        self._read_csv()

    @logger.catch
    def _read_csv(self):
        self._csv_file = csv.reader(open(self._path, encoding='utf-8-sig'))
        for row in self._csv_file:
            if row == [] or "#" in row[0]:
                logger.debug(f"Del:{row}")
            else:
                self._raw.append(row)
        self._raw = self._raw[1:]
        logger.debug(f"Loaded [{self._path}]")
        logger.debug(f"Rows in [{self._path}]:{len(self._raw)}")

    @logger.catch
    def refresh(self):
        self._raw.clear()
        self._read_csv()
        logger.debug(f"Refreshed [{self._path}]")

    def studentID(self, i):
        return self._raw[i][0]

    def password(self, i):
        return self._raw[i][1]

    def wechat_push(self, i):
        return self._raw[i][2]

    def email_push(self, i):
        return self._raw[i][3]

    def sendkey(self, i):
        return self._raw[i][4]

    def userid(self, i):
        return self._raw[i][5]

    def email(self, i):
        return self._raw[i][6]

    @property
    def row(self):
        return len(self._raw)


global_account = Account(gc.config('/config/path/account_file'))
