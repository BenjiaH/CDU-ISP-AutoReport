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
        self._all_info = self.get_info()
        self._len = len(self._all_info[0])

    def get_info(self):
        ret = [[], [], [], [], []]
        for item in self._account:
            for i in range(5):
                ret[i].append(item[i])
        for i in range(5):
            ret[i][:] = ret[i][1:]
        return ret

    @property
    def studentID(self):
        return self._all_info[0]

    @property
    def password(self):
        return self._all_info[1]

    @property
    def method(self):
        return self._all_info[2]

    @property
    def sckey(self):
        return self._all_info[3]

    @property
    def email(self):
        return self._all_info[4]

    @property
    def len(self):
        return self._len


global_account = Account()
print(global_account.studentID)
print(global_account.password)
print(global_account.sckey)
