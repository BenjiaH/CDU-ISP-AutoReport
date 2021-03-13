import requests
import re

from datetime import datetime
from common import security
from common.logger import logger


class Report:
    def __init__(self):
        self._session = 0
        self._host = 0
        self._headers = 0
        self._main_host = "https://xsswzx.cdu.edu.cn/"
        self._id_value = 0
        self._date = ""
        self._captcha_code = ""

    def update_date(self):
        today = datetime.now()
        today = "{y}年{m}月{d}日".format(y=today.year, m=today.month, d=today.day)
        self._date = today

    def _get_captcha_code(self):
        url = "{host}/com_user/weblogin.asp".format(host=self._host)
        res = self._session.get(url=url, headers=self._headers)
        res.encoding = "utf-8"
        captcha_index = res.text.find('placeholder="验证码"')
        self._captcha_code = res.text[captcha_index + 30: captcha_index + 34]

    def _login(self, uid, password, code):
        url = "{host}/com_user/weblogin.asp".format(host=self._host)
        data = {
            "username": uid,
            "userpwd": password,
            "code": code,
            "login": "login",
            "checkcode": "1",
            "rank": "0",
            "action": "login",
            "m5": "1",
        }
        res = self._session.post(url=url, headers=self._headers, data=data)
        if res.status_code != 200:
            logger.error("POST request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))

    def _get_id(self):
        url = "{host}/com_user/left.asp".format(host=self._host)
        res = self._session.get(url=url, headers=self._headers)
        if res.status_code != 200:
            logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        res.encoding = "utf-8"
        try:
            self._id_value = re.findall(r"(?<=id=).*?(?=\">我的事务<)", res.text)[0]
            logger.info("Login successfully.")
        except Exception as e:
            self._id_value = 0
            logger.error("Regular expression match failed.[{e}]".format(e=e))
            logger.error("Login failed.")

    def _report(self):
        if self._id_value == 0:
            return
        url = "{host}/com_user/project_addx.asp?id={id}&id2={id2}".format(
            host=self._host, id=self._id_value, id2=self._date)
        logger.info("Get report url.")
        res = self._session.get(url=url, headers=self._headers)
        if res.status_code != 200:
            logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))

    def _is_reported(self):
        if self._id_value == 0:
            return
        url = "{host}/com_user/project.asp?id={id}".format(
            host=self._host, id=self._id_value)
        res = self._session.get(url=url, headers=self._headers)
        if res.status_code != 200:
            logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
            return
        res.encoding = "utf-8"
        # host refreshes records every months(1st day of this month)
        if "还没有登记记录" in res.text:
            logger.info("Report is not existed.")
            return False
        try:
            latest_date = re.findall(r"(?<=<td class=\"tdmenu\"><div align=\"center\">).*?(?=</div></td>)", res.text)[0]
        except Exception as e:
            logger.error("Regular expression match failed.[{e}]".format(e=e))
            return
        if latest_date == self._date:
            logger.info("Report is existed.")
            return True
        else:
            logger.info("Report is not existed.")
            return False

    def main(self, uid, password):
        self._session = requests.Session()
        self._host = self._main_host + security.get_random_host()
        self._headers = {
            "User-Agent": security.get_random_useragent()
        }
        self._get_captcha_code()
        self._login(uid, password, self._captcha_code)
        self._get_id()
        if self._is_reported():
            logger.info("Report is already existed. ID:{uid}".format(uid=uid))
            return 0
        else:
            self._report()
            if self._is_reported():
                logger.info("Report successfully. ID:{uid}".format(uid=uid))
                return 1
            else:
                logger.error("Report failed. ID:{uid}".format(uid=uid))
                return 2
