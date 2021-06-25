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
            logger.debug("{url} text:\n{res}".format(url=url, res=res.content))
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
            logger.error("Failed:POST request. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))

    @logger.catch
    def _get_project_url(self):
        url = "{host}/left.asp".format(host=self._host)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("Failed:GET request. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            self._project_url = soup.find('a', string="疫情信息登记")['href']
            logger.info("Successful to login the ISP.")
            logger.debug("Project url:{url}.".format(url=self._project_url))
        except Exception as e:
            self._error = 1
            logger.debug("Set the error flag to {err_flag}.".format(err_flag=self._error))
            logger.error("Failed to get the id value.[{e}]".format(e=e))
            logger.error("Failed to login the ISP.")
            logger.debug("{url} text:\n{res}".format(url=url, res=res.content))

    @logger.catch
    def _get_report_url(self):
        if self._error == 1:
            logger.debug("The error flag:{err_flag}.Exit.".format(err_flag=self._error))
            return
        url = "{host}/{project}".format(host=self._host, project=self._project_url)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("Failed:GET request. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            self._report_url = soup.find(value="【一键登记：无变化】").parent['href']
            logger.info("Get the report url.")
            logger.debug("The report url:{url}.".format(url=self._report_url))
        except Exception as e:
            self._error = 1
            logger.debug("Set the error flag to {err_flag}.".format(err_flag=self._error))
            logger.error("Failed to get the report url.[{e}]".format(e=e))
            logger.debug("{url} text:\n{res}".format(url=url, res=res.content))

    @logger.catch
    def _report(self):
        if self._error == 1:
            logger.debug("The error flag:{err_flag}.Exit.".format(err_flag=self._error))
            return
        url = "{host}/{report}".format(host=self._host, report=self._report_url)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("Failed:GET request. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))

    @logger.catch
    def _parse_records(self, page_text):
        soup = BeautifulSoup(page_text, 'lxml')
        try:
            record_val = soup.find("td", class_="tdmenu").text.strip()
            if "年" not in record_val:
                record_val = soup.find("table", class_="table table-hover").find_all("div", align="center")[
                    8].text.strip()
            logger.debug("The record value:{val}".format(val=record_val))
        except Exception as e:
            logger.error("Failed to get the latest record value. [{e}]".format(e=e))
            self._errno = 5
            logger.debug("Set the error code to {errno}.".format(errno=self._errno))
            return False
        return record_val

    @logger.catch
    def _is_reported(self):
        if self._error == 1:
            logger.debug("The error flag:{err_flag}.Exit.".format(err_flag=self._error))
            return
        url = "{host}/{project}".format(host=self._host, project=self._project_url)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("Failed:GET request. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
            return
        res.encoding = "utf-8"
        record_val = self._parse_records(res.text)
        if not record_val:
            logger.debug("{url} text:\n{res}".format(url=url, res=res.content))
            return False
        elif record_val == self._date:
            logger.info("Check:the report is existed.")
            return True
        else:
            logger.info("Check:the report is not existed.")
            return False

    @logger.catch
    def main(self, uid, password):
        self._error = 0
        self._session = requests.Session()
        self._host = self._main_host + security.get_random_host() + "/com_user"
        self._headers = {
            "User-Agent": security.get_random_useragent()
        }
        self._get_captcha_code()
        self._login(uid, password)
        self._get_project_url()
        if self._is_reported():
            logger.info("The report is already existed. ID:{uid}".format(uid=uid))
            return 0
        else:
            logger.info("Try to report.")
            self._get_report_url()
            self._report()
            if self._is_reported():
                logger.info("Successful to report. ID:{uid}".format(uid=uid))
                return 1
            else:
                logger.error("Failed to report. ID:{uid}".format(uid=uid))
                return 2
