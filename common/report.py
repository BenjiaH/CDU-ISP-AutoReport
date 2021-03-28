import requests

from datetime import datetime
from common import security
from common.logger import logger
from bs4 import BeautifulSoup


class Report:
    def __init__(self):
        self._error = 0
        self._session = 0
        self._host = 0
        self._headers = 0
        self._main_host = "https://xsswzx.cdu.edu.cn/"
        self._project_url = 0
        self._report_url = 0
        self._date = ""
        self._captcha_code = ""

    @logger.catch
    def update_date(self):
        today = datetime.now()
        today = "{y}年{m}月{d}日".format(y=today.year, m=today.month, d=today.day)
        self._date = today
        logger.debug("Date:{today}".format(today=self._date))

    @logger.catch
    def _get_captcha_code(self):
        url = "{host}/weblogin.asp".format(host=self._host)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            code = soup.find(id="code").parent.text.strip()
        except Exception as e:
            logger.error("Get captcha code failed. [{e}]".format(e=e))
            logger.debug("{url} text:\n{res}".format(url=url, res=res.text))
            code = 0
        self._captcha_code = code

    @logger.catch
    def _login(self, uid, password):
        url = "{host}/weblogin.asp".format(host=self._host)
        data = {
            "username": uid,
            "userpwd": password,
            "code": self._captcha_code,
            "login": "login",
            "checkcode": "1",
            "rank": "0",
            "action": "login",
            "m5": "1",
        }
        res = self._session.post(url=url, headers=self._headers, data=data)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("POST request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))

    @logger.catch
    def _get_project_url(self):
        url = "{host}/left.asp".format(host=self._host)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            self._project_url = soup.find('a', string="疫情信息登记")['href']
            logger.info("Login successfully.")
            logger.debug("Project url:{url}.".format(url=self._project_url))
        except Exception as e:
            self._error = 1
            logger.error("Get id value failed.[{e}]".format(e=e))
            logger.error("Login failed.")
            logger.debug("{url} text:\n{res}".format(url=url, res=res.text))

    @logger.catch
    def _get_report_url(self):
        if self._error == 1:
            return
        url = "{host}/{project}".format(host=self._host, project=self._project_url)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            self._report_url = soup.find(value="【一键登记：无变化】").parent['href']
            logger.info("Get report url.")
            logger.debug("Report url:{url}.".format(url=self._report_url))
        except Exception as e:
            self._error = 1
            logger.error("Get report url failed.[{e}]".format(e=e))
            logger.debug("{url} text:\n{res}".format(url=url, res=res.text))

    @logger.catch
    def _report(self):
        if self._error == 1:
            return
        url = "{host}/{report}".format(host=self._host, report=self._report_url)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))

    @logger.catch
    def _is_reported(self):
        if self._error == 1:
            return
        url = "{host}/{project}".format(host=self._host, project=self._project_url)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
            return
        res.encoding = "utf-8"
        # host refreshes records every months(1st day of this month)
        if "还没有登记记录" in res.text:
            logger.info("Report is not existed.")
            return False
        else:
            try:
                soup = BeautifulSoup(res.text, 'lxml')
                latest_date = soup.find("td", class_="tdmenu").text
            except Exception as e:
                logger.error("Get the latest date failed. [{e}]".format(e=e))
                logger.debug("{url} text:\n{res}".format(url=url, res=res.text))
                return
            if latest_date == self._date:
                logger.info("Report is existed.")
                return True
            else:
                logger.info("Report is not existed.")
                return False

    @logger.catch
    def main(self, uid, password):
        self._session = requests.Session()
        self._host = self._main_host + security.get_random_host() + "/com_user"
        self._headers = {
            "User-Agent": security.get_random_useragent()
        }
        self._get_captcha_code()
        self._login(uid, password)
        self._get_project_url()
        self._get_report_url()
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
