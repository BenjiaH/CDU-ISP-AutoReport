import re
import requests

from urllib import parse
from bs4 import BeautifulSoup
from common.utils import utils
from common.logger import logger
from common.config import config


class Report:
    @logger.catch
    def __init__(self):
        self._error = 0
        self._errno = 0
        self._session = 0
        self._host = 0
        self._headers = 0
        self._navigation_url = 0
        self._captcha_code = ""
        self._login_url = None
        self._left_url = None
        self._navigation_target = None
        self._default_report_url = None
        self._report_url = None
        self._host_0 = None
        self._host_1 = None
        self._success = None
        self._existed = None
        self.fetch_param()

    @logger.catch
    def fetch_param(self):
        self._login_url = config.config('/config/url/login', utils.get_call_loc())
        self._left_url = config.config('/config/url/left', utils.get_call_loc())
        self._navigation_target = config.config('/config/url/navigation', utils.get_call_loc())
        self._default_report_url = config.config('/config/url/report_default', utils.get_call_loc())
        self._report_url = config.config('/config/url/report', utils.get_call_loc())
        self._host_0 = config.config('/config/url/host_head', utils.get_call_loc())
        self._host_1 = config.config('/config/url/host_foot', utils.get_call_loc())
        self._success = config.config('/config/response/success', utils.get_call_loc())
        self._existed = config.config('/config/response/existed', utils.get_call_loc())
        logger.debug("Fetched [Report] params.")

    @logger.catch
    def _set_error(self, no, flag, func):
        self._errno = no
        logger.debug(f"[{func}] Set the error code: {self._errno}.")
        self._error = flag
        logger.debug(f"[{func}] Set the error flag: {self._error}.")

    @logger.catch
    def _get_captcha_code(self):
        if len(utils.available_host) == 0:
            logger.error(f"No available hosts.")
            self._set_error(4, 1, utils.get_call_loc(True))
            return
        url = f"{self._host}/{self._login_url}"
        res = self._session.get(url=url, headers=self._headers)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            code = soup.find(id="code").parent.text.strip()
            logger.debug(f"Verification code: {code}")
        except Exception as e:
            logger.error(f"Failed to get the captcha code. [{e}]")
            self._set_error(1, 1, utils.get_call_loc(True))
            code = 0
            logger.debug("{url} content:\n{res}".format(url=url, res=re.sub(r"\n|\r|\t|\s", "", res.text)))
        self._captcha_code = code

    @logger.catch
    def _login(self, uid, password):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        url = f"{self._host}/{self._login_url}"
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
        payload["userpwd"] = "*******"
        logger.debug(f"URL:{url}. Payload:{payload}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        if res.status_code != 200:
            logger.error(f"Failed:POST request. URL:{url}. Status code:{res.status_code}")
            self._set_error(2, 1, utils.get_call_loc(True))
        elif "alert" in res.text:
            logger.error("Failed to login the CDU-ISP.[Incorrect username, password or captcha code]")
            self._set_error(2, 1, utils.get_call_loc(True))
        else:
            logger.info("Successful to login the CDU-ISP.")

    @logger.catch
    def _get_navigation_url(self, target):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        url = f"{self._host}/{self._left_url}"
        res = self._session.get(url=url, headers=self._headers)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            self._navigation_url = soup.find('a', string=target)['href']
            logger.debug(f'Navigation "{target}" url:{self._navigation_url}.')
        except Exception as e:
            logger.error(f"Failed to get the project url.[{e}]")
            self._set_error(3, 1, utils.get_call_loc(True))
            logger.debug("{url} content:\n{res}".format(url=url, res=re.sub(r"\n|\r|\t|\s", "", res.text)))

    @logger.catch
    def _report_default_method(self):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return ""
        logger.info("Try to report in the default method.")
        param = parse.parse_qs(parse.urlparse(str(self._navigation_url)).query)
        url = f"{self._host}/{self._default_report_url}"
        payload = {
            "id": param["id"][0],
            "id2": utils.date,
            "adds": "undefined",
            "addsxy": "undefined"
        }
        res = self._session.get(url=url, headers=self._headers, data=payload)
        payload["id"] = "*******"
        logger.debug(f"URL:{url}. Payload:{payload}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        return res.text

    @logger.catch
    def _report(self, location):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return ""
        logger.info("Try to report in the alternate method.")
        [province, city, area] = location
        param = parse.parse_qs(parse.urlparse(str(self._navigation_url)).query)
        url = f"{self._host}/{self._report_url}"
        payload = {
            "id": param["id"][0],
            "id2": utils.date,
            "province": province,
            "city": city,
            "area": area,
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
        res = self._session.post(url=url, headers=self._headers, data=payload)
        payload["id"] = "*******"
        logger.debug(f"URL:{url}. Payload:{payload}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        return res.text

    @logger.catch
    def _fetch_location(self):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return ["", "", ""]
        for i in range(2):
            url = f"{self._host}/{self._navigation_url}&page={i + 1}"
            res = self._session.get(url=url, headers=self._headers)
            logger.debug(f"URL:{url}. Status code:{res.status_code}")
            if res.status_code != 200:
                logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
            res.encoding = "utf-8"
            try:
                soup = BeautifulSoup(res.text, 'lxml')
                location = soup.find("table", class_="table table-hover").find_all("tr")[3].find_all("td")[
                    1].text.strip()
                logger.debug(f'location: "{location}"')
                return location.split("|")
            except Exception as e:
                if i != 2:
                    logger.error(f"Failed to get the location. Try next page.[{e}]")
                else:
                    logger.error(f"Failed to get the location.[{e}]")
                    self._set_error(5, 1, utils.get_call_loc(True))
                logger.debug("{url} content:\n{res}".format(url=url, res=re.sub(r"\n|\r|\t|\s", "", res.text)))

    @logger.catch
    def main(self, uid, password):
        self._error = 0
        self._errno = 0
        self._session = requests.Session()
        self._host = f"{self._host_0}/{utils.get_random_host()}/{self._host_1}"
        self._headers = {
            "User-Agent": utils.get_random_useragent()
        }
        self._get_captcha_code()
        self._login(uid, password)
        self._get_navigation_url(self._navigation_target)
        ret = self._report_default_method()
        if self._existed in ret:
            logger.info(f"The report is already existed. ID:{uid}")
            return 0, self._errno
        elif self._success in ret:
            logger.info(f"Successful to report. ID:{uid}")
            return 1, self._errno
        else:
            logger.error("Failed to report in the default method.")
            ret = self._report(self._fetch_location())
            if self._existed in ret:
                logger.info(f"The report is already existed. ID:{uid}")
                return 0, self._errno
            elif self._success in ret:
                logger.info(f"Successful to report. ID:{uid}")
                return 1, self._errno
            else:
                logger.error("Failed to report in the alternate method.")
                logger.error(f"Failed to report. ID:{uid}")
                if self._errno == 0:
                    self._set_error(-1, self._error, utils.get_call_loc(True))
                return 2, self._errno


report = Report()
