import re
import requests

from urllib import parse
from datetime import datetime
from bs4 import BeautifulSoup
from common import security
from common.logger import logger


class Report:
    def __init__(self):
        self._error = 0
        self._errno = 0
        self._session = 0
        self._host = 0
        self._headers = 0
        self._main_host = "https://xsswzx.cdu.edu.cn/"
        self._navigation_url = 0
        self._report_url = 0
        self._date = ""
        self._captcha_code = ""

    @logger.catch
    def update_date(self):
        today = datetime.now()
        today = f"{today.year}年{today.month}月{today.day}日"
        self._date = today
        logger.debug(f"Date:{self._date}")

    @logger.catch
    def _get_captcha_code(self):
        if len(security.available_host) == 0:
            logger.error(f"Failed to establish a new connection.")
            self._errno = 6
            logger.debug(f"Set the error code: {self._errno}.")
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")
            return
        url = f"{self._host}/weblogin.asp"
        res = self._session.get(url=url, headers=self._headers)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            code = soup.find(id="code").parent.text.strip()
            logger.debug(f"Verification code: {code}")
        except Exception as e:
            logger.error(f"Failed to get the captcha code. [{e}]")
            self._errno = 1
            logger.debug(f"Set the error code: {self._errno}.")
            code = 0
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")
            logger.debug("{url} content:\n{res}".format(url=url, res=re.sub(r"\n|\r|\t|\s", "", res.text)))
        self._captcha_code = code

    @logger.catch
    def _login(self, uid, password):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        url = f"{self._host}/weblogin.asp"
        payload = {
            "username": uid,
            "userpwd": password,
            "code": self._captcha_code,
            "login": "login",
            "checkcode": "1",
            "rank": "0",
            "action": "login",
            "m5": "1",
        }
        res = self._session.post(url=url, headers=self._headers, data=payload)
        res.encoding = "utf-8"
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:POST request. URL:{url}. Status code:{res.status_code}")
        if "学号或密码错误" in res.text:
            logger.error("Failed to login the ISP.[Incorrect username or password]")
            logger.debug("Failed to login the ISP.[Incorrect username or password]")
            self._errno = 2
            logger.debug(f"Set the error code: {self._errno}.")
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")

    @logger.catch
    def _get_navigation_url(self, target):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        url = f"{self._host}/left.asp"
        res = self._session.get(url=url, headers=self._headers)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            self._navigation_url = soup.find('a', string=target)['href']
            logger.info("Successful to login the ISP.")
            logger.debug(f"Project url:{self._navigation_url}.")
        except Exception as e:
            logger.error(f"Failed to get the project url.[{e}]")
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")
            self._errno = 3
            logger.debug(f"Set the error code: {self._errno}.")
            logger.debug("{url} content:\n{res}".format(url=url, res=re.sub(r"\n|\r|\t|\s", "", res.text)))

    @logger.catch
    def _get_report_url(self):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        url = f"{self._host}/{self._navigation_url}"
        res = self._session.get(url=url, headers=self._headers)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            t_url = str(soup.find_all("script", type="text/javascript")[2]).replace("\r\n", "")
            report_url = t_url[t_url.find("href=") + 6: -11]
            self._report_url = report_url.replace('"+adds2+"', "undefined").replace('"+addsxy2', "undefined")
            logger.info("Get the report url.")
            logger.debug(f"The report url:{self._report_url}.")
        except Exception as e:
            logger.error(f"Failed to get the report url.")
            logger.error(f'[{e.__traceback__.tb_frame.f_globals["__file__"]}.{e.__traceback__.tb_lineno}:{e}]')
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")
            self._errno = 4
            logger.debug(f"Set the error code: {self._errno}.")
            logger.debug("{url} content:\n{res}".format(url=url, res=re.sub(r"\n|\r|\t|\s", "", res.text)))

    @logger.catch
    def _report_default_method(self):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        param = parse.parse_qs(parse.urlparse(str(self._navigation_url)).query)
        url = f"{self._host}/project_addx.asp"
        payload = {
            "id": param["id"],
            "id2": self._date,
            "adds": "undefined",
            "addsxy": "undefined"
        }
        res = self._session.get(url=url, headers=self._headers, data=payload)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        return res.text

    @logger.catch
    def _report(self):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        param = parse.parse_qs(parse.urlparse(str(self._navigation_url)).query)
        url = f"{self._host}/project_add.asp"
        payload = {
            "id": param["id"],
            "province": "四川省",
            "city": "成都市",
            "area": "龙泉驿区",
            "wuhan": "否",
            "fare": "否",
            "wls": "否",
            "kesou": "否",
            "zhengduan": "",
            "Submit": "提交",
            "action": "add",
            "adds": "undefined",
            "addsxy": "undefined"
        }
        res = self._session.get(url=url, headers=self._headers, data=payload)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        return res.text

    @logger.catch
    def main(self, uid, password):
        self._error = 0
        self._errno = 0
        self._session = requests.Session()
        self._host = self._main_host + security.get_random_host() + "/com_user"
        self._headers = {
            "User-Agent": security.get_random_useragent()
        }
        self._get_captcha_code()
        self._login(uid, password)
        self._get_navigation_url("疫情信息登记")
        logger.info("Try to report in default the method.")
        ret = self._report_default_method()
        if "已存在" in ret:
            logger.info(f"The report is already existed. ID:{uid}")
            return 0, self._errno
        elif "提交成功" in ret:
            logger.info(f"Successful to report. ID:{uid}")
            return 1, self._errno
        else:
            logger.error("Failed to report in the default method.Try to report in the alternate method.")
            ret = self._report()
            if "已存在" in ret:
                logger.info(f"The report is already existed. ID:{uid}")
                return 0, self._errno
            elif "提交成功" in ret:
                logger.info(f"Successful to report. ID:{uid}")
                return 1, self._errno
            else:
                logger.error(f"Failed to report. ID:{uid}")
                if self._errno == 0:
                    self._errno = 7
                    logger.debug(f"Set the error code: {self._errno}.")
                return 2, self._errno
