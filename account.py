import os
import csv

from logger import logger


class Account(object):
    def __init__(self, csv_file="account.csv"):
        self._path = os.path.join(os.getcwd(), csv_file)
        if not os.path.exists(self._path):
            logger.error("No such file: account.csv")
            raise FileNotFoundError("No such file: account.csv")
        self._csv_file = open(self._path, encoding='utf-8')
        self._account = csv.reader(self._csv_file)
        self._row = sum(1 for line in open(self._path, encoding='utf-8')) - 1
        self._col = len(next(self._account))
        self._all_info = self.get_info()

    def refresh(self):
        self._csv_file = open(self._path, encoding='utf-8')
        self._account = csv.reader(self._csv_file)
        self._row = sum(1 for line in open(self._path, encoding='utf-8')) - 1
        self._col = len(next(self._account))
        self._all_info = self.get_info()

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
    def sckey(self):
        return self._all_info[4]

    @property
    def email(self):
        return self._all_info[5]

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col


global_account = Account()
