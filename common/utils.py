import os
import random
import requests
import sys

from common.logger import logger
from common.config import config
from fake_useragent import UserAgent
from datetime import datetime


class Utils:
    @logger.catch
    def __init__(self):
        self._HOSTS = None
        self._url_0 = None
        self._url_2 = None
        self._url_3 = None
        self.fetch_param()
        self._ua = UserAgent(verify_ssl=False)
        self.available_host = []
        self.date = ""

    @logger.catch
    def fetch_param(self):
        self._HOSTS = list(config.config('/config/all_hosts', self.get_call_loc()).keys())
        self._url_0 = config.config('/config/url/host_head', self.get_call_loc())
        self._url_2 = config.config('/config/url/host_foot', self.get_call_loc())
        self._url_3 = config.config('/config/url/login', self.get_call_loc())
        logger.debug("Fetched [Utils] params.")

    @logger.catch
    def _check_host_status(self, host):
        url = f"{self._url_0}/{host}/{self._url_2}/{self._url_3}"
        try:
            res = requests.get(url=url, timeout=5)
            logger.debug(f"URL:{url}. Status code:{res.status_code}")
        except Exception as e:
            logger.error(f'Failed to connect to the server "{host}". [{e}]')
            return False
        res.encoding = "utf-8"
        if "updatenow.asp" in res.text:
            logger.error(f'Failed to connect to the server "{host}". [updating]')
            return False
        elif res.status_code != 200:
            logger.error(f'Failed to connect to the server "{host}". [Status code:{res.status_code}]')
            return False
        else:
            return True

    @logger.catch
    def refresh_hosts(self):
        self.available_host.clear()
        for i in self._HOSTS:
            if self._check_host_status(i):
                self.available_host.append(i)
        logger.info("Successful to check hosts status.")
        if len(self.available_host) == 0:
            logger.error("Available host:[None].")
        elif len(self.available_host) != len(self._HOSTS):
            logger.error(f"Available host:{self.available_host}.")

    @logger.catch
    def get_random_useragent(self):
        random_ua = self._ua.random
        logger.debug(f"User Agent:{random_ua}")
        return random_ua

    @logger.catch
    def get_random_host(self):
        try:
            ret_host = random.choice(self.available_host)
            logger.debug(f'Random host:"{ret_host}".')
        except Exception as e:
            logger.error(e)
            return ""
        return ret_host

    @staticmethod
    @logger.catch
    def version(version):
        num, stage = version.split("|")
        if os.path.exists("../.git"):
            logger.debug(f'Founded [{os.path.abspath("../.git")}]')
            commit_id = (os.popen("git rev-parse --short HEAD").read()).replace("\n", "")
            commit_id = "." + commit_id
        else:
            commit_id = ""
        if stage != "":
            stage = f"({stage})"
        info = f"{num}{commit_id}{stage}"
        logger.info(f"Version:{info}")

    @staticmethod
    def get_call_loc(func=False):
        file_name = os.path.basename(sys._getframe().f_back.f_code.co_filename)
        line = sys._getframe().f_back.f_lineno
        if func:
            func_name = sys._getframe().f_back.f_code.co_name
            return f"{file_name}:{func_name}:{line}"
        else:
            return f"{file_name}:{line}"

    @logger.catch
    def update_date(self):
        today = datetime.now()
        today = f"{today.year}年{today.month}月{today.day}日"
        self.date = today
        logger.debug(f"Date:{self.date}")

    @logger.catch
    def refresh_param(self):
        from common.service import report_service
        report_service.fetch_param()
        from common.report import report
        report.fetch_param()
        from common.push import push
        push.fetch_param()
        push.bot_email.fetch_param()
        self.fetch_param()


utils = Utils()
