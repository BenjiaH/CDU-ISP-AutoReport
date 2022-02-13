import re
import requests

from datetime import datetime
from common import security
from common.logger import logger
from bs4 import BeautifulSoup


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
        self.class_dict = {}
        self.not_reported_stu_dict = {}

    @logger.catch
    def update_date(self):
        today = datetime.now()
        today = f"{today.year}年{today.month}月{today.day}日"
        self._date = today
        logger.debug(f"Date:{self._date}")

    @logger.catch
    def _get_captcha_code(self):
        url = f"{self._host}/weblogin.asp"
        try:
            res = self._session.get(url=url, headers=self._headers)
            logger.debug(f"URL:{url}. Status code:{res.status_code}")
            res.encoding = "utf-8"
        except Exception as e:
            logger.error(f"Failed to establish a new connection. [{e}]")
            self._errno = 6
            logger.debug(f"Set the error code: {self._errno}.")
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")
            return
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            code = soup.find(id="code").parent.text.strip()[:4]
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
        data = {
            "username": uid,
            "userpwd": password,
            "code": self._captcha_code,
            "login": "login",
            "checkcode": "1",
            "rank": "4",
            "action": "login",
            "m5": "1",
        }
        res = self._session.post(url=url, headers=self._headers, data=data)
        res.encoding = "utf-8"
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:POST request. URL:{url}. Status code:{res.status_code}")
            self._errno = 2
            logger.debug(f"Set the error code: {self._errno}.")
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")
        elif "重新登陆" in res.text:
            logger.error("Failed to login the ISP.[Incorrect username, password or captcha code]")
            logger.debug("Failed to login the ISP.[Incorrect username, password or captcha code]")
            self._errno = 2
            logger.debug(f"Set the error code: {self._errno}.")
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")
        else:
            logger.info("Successful to login the ISP.")

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
            logger.debug(f"Navigation url:{self._navigation_url}.")
        except Exception as e:
            logger.error(f"Failed to get the navigation url.[{e}]")
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")
            self._errno = 7
            logger.debug(f"Set the error code: {self._errno}.")
            logger.debug("{url} content:\n{res}".format(url=url, res=re.sub(r"\n|\r|\t|\s", "", res.text)))

    @logger.catch
    def _get_class_info(self):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        url = f"{self._host}/{self._navigation_url}"
        payload = {
            "coded": self._date
        }
        res = self._session.get(url=url, headers=self._headers, data=payload)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            classname = soup.find_all("select", size="1")[-1].text.strip()
            classname = classname.split("\n")
            for i in classname:
                self.class_dict[i] = soup.find('option', string=i)['value'].strip()
            logger.info("Successful to get the class info.")
            logger.debug(f"The class info:{self.class_dict}.")
        except Exception as e:
            logger.error(f"Failed to get the classed info.[{e}]")
            self._error = 1
            logger.debug(f"Set the error flag: {self._error}.")
            self._errno = 8
            logger.debug(f"Set the error code: {self._errno}.")
            logger.debug("{url} content:\n{res}".format(url=url, res=re.sub(r"\n|\r|\t|\s", "", res.text)))

    @logger.catch
    def _get_not_reported_stu(self):
        for i in self.class_dict:
            if self._error == 1:
                logger.debug(f"The error flag: {self._error}. Exit the function.")
                return
            url = f"{self._host}/{self._navigation_url}"
            payload = {
                "coded": self._date,
                "class_id": self.class_dict[i],
                "submit": "查询"
            }
            res = self._session.get(url=url, headers=self._headers, data=payload)
            logger.debug(f"URL:{url}. Status code:{res.status_code}")
            if res.status_code != 200:
                logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
            res.encoding = "utf-8"
            try:
                soup = BeautifulSoup(res.text, 'lxml')
                stu = ""
                t = soup.find_all("table", class_="atable1")[3]
                if "完成" in t.text:
                    stu = "无"
                else:
                    t = t.find_all("td")[1].find_all(size=2)
                    for j in t:
                        if j.text in ["[同步][登记]", "同步", "[登记]"]:
                            pass
                        else:
                            stu = j.text + "、" + stu
                    stu = stu[:-1]
                self.not_reported_stu_dict[i] = stu
            except Exception as e:
                logger.error(f"Failed to get the not reported students list.[{e}]")
                self._error = 1
                logger.debug(f"Set the error flag: {self._error}.")
                self._errno = 9
                logger.debug(f"Set the error code: {self._errno}.")
                logger.debug("{url} content:\n{res}".format(url=url, res=re.sub(r"\n|\r|\t|\s", "", res.text)))
        logger.info("Successful to get the not reported students list.")
        logger.debug(self.not_reported_stu_dict)

    @logger.catch
    def main(self, uid, password):
        self.class_dict = {}
        self.not_reported_stu_dict = {}
        self._error = 0
        self._errno = 0
        self._session = requests.Session()
        self._host = self._main_host + security.get_random_host()
        self._headers = {
            "User-Agent": security.get_random_useragent()
        }
        self._get_captcha_code()
        self._login(uid, password)
        self._get_navigation_url("信息解析")
        self._get_class_info()
        self._get_navigation_url("疫情登记情况")
        self._get_not_reported_stu()
        if self._errno != 0:
            return 2, self._errno, None
        else:
            return 1, self._errno, self.not_reported_stu_dict
