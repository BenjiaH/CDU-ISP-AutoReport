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
        try:
            res = self._session.get(url=url, headers=self._headers)
            logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
            res.encoding = "utf-8"
        except Exception as e:
            logger.error("Failed to establish a new connection. [{e}]".format(e=e))
            self._errno = 6
            logger.debug("Set the error code: {errno}.".format(errno=self._errno))
            self._error = 1
            logger.debug("Set the error flag: {err_flag}.".format(err_flag=self._error))
            return
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            code = soup.find(id="code").parent.text.strip()
        except Exception as e:
            logger.error("Failed to get the captcha code. [{e}]".format(e=e))
            self._errno = 1
            logger.debug("Set the error code: {errno}.".format(errno=self._errno))
            logger.debug("{url} text:\n{res}".format(url=url, res=res.content))
            code = 0
            self._error = 1
            logger.debug("Set the error flag: {err_flag}.".format(err_flag=self._error))
        self._captcha_code = code

    @logger.catch
    def _login(self, uid, password):
        if self._error == 1:
            logger.debug("The error flag: {err_flag}. Exit the function.".format(err_flag=self._error))
            return
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
        res.encoding = "utf-8"
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("Failed:POST request. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if "学号或密码错误" in res.text:
            logger.error("Failed to login the ISP.[Incorrect username or password]")
            logger.debug("Failed to login the ISP.[Incorrect username or password]")
            self._errno = 2
            logger.debug("Set the error code: {errno}.".format(errno=self._errno))
            self._error = 1
            logger.debug("Set the error flag: {err_flag}.".format(err_flag=self._error))

    @logger.catch
    def _get_project_url(self):
        if self._error == 1:
            logger.debug("The error flag: {err_flag}. Exit the function.".format(err_flag=self._error))
            return
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
            logger.error("Failed to get the project url.[{e}]".format(e=e))
            self._error = 1
            logger.debug("Set the error flag: {err_flag}.".format(err_flag=self._error))
            self._errno = 3
            logger.debug("Set the error code: {errno}.".format(errno=self._errno))
            logger.debug("{url} text:\n{res}".format(url=url, res=res.content))

    @logger.catch
    def _get_report_url(self):
        if self._error == 1:
            logger.debug("The error flag: {err_flag}. Exit the function.".format(err_flag=self._error))
            return
        url = "{host}/{project}".format(host=self._host, project=self._project_url)
        res = self._session.get(url=url, headers=self._headers)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        if res.status_code != 200:
            logger.error("Failed:GET request. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        res.encoding = "utf-8"
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            t_url = str(soup.find_all("script", type="text/javascript")[2]).replace("\r\n", "")
            report_url = t_url[t_url.find("href=") + 6: -11]
            self._report_url = report_url.replace('"+adds2+"', "undefined").replace('"+addsxy2', "undefined")
            logger.info("Get the report url.")
            logger.debug("The report url:{url}.".format(url=self._report_url))
        except Exception as e:
            logger.error("Failed to get the report url.[{e}]".format(e=e))
            self._error = 1
            logger.debug("Set the error flag: {err_flag}.".format(err_flag=self._error))
            self._errno = 4
            logger.debug("Set the error code: {errno}.".format(errno=self._errno))
            logger.debug("{url} text:\n{res}".format(url=url, res=res.content))

    @logger.catch
    def _report(self):
        if self._error == 1:
            logger.debug("The error flag: {err_flag}. Exit the function.".format(err_flag=self._error))
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
            logger.debug("The record value:{val}".format(val=record_val))
            if "年" not in record_val and "还没有登记记录" not in record_val:
                raise Exception("Can not parse the latest record value")
        except Exception as e:
            logger.debug("Failed to get the latest record value. [{e}. Try to change the parse rule.]".format(e=e))
            try:
                record_val = soup.find("table", class_="table table-hover").find_all("tr")[
                    3].find("div", align="center").text.strip()
                logger.debug("The record value:{val}".format(val=record_val))
                if "年" not in record_val and "还没有登记记录" not in record_val:
                    raise Exception("Can not parse the latest record value.")
            except Exception as e:
                logger.error("Failed to get the latest record value. [{e}]".format(e=e))
                self._errno = 5
                logger.debug("Set the error code: {errno}.".format(errno=self._errno))
                return False
        return record_val

    @logger.catch
    def _is_reported(self):
        if self._error == 1:
            logger.debug("The error flag: {err_flag}. Exit the function.".format(err_flag=self._error))
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
            logger.info("Check:the latest report is not existed.")
            logger.debug("{url} text:\n{res}".format(url=url, res=res.content))
            return False
        elif record_val == self._date:
            logger.info("Check:the latest report is existed.")
            return True
        else:
            logger.info("Check:the latest report is not existed.")
            return False

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
        self._get_project_url()
        if self._is_reported():
            logger.info("The report is already existed. ID:{uid}".format(uid=uid))
            return 0, self._errno
        else:
            logger.info("Try to report.")
            self._get_report_url()
            self._report()
            if self._is_reported():
                logger.info("Successful to report. ID:{uid}".format(uid=uid))
                return 1, self._errno
            else:
                logger.error("Failed to report. ID:{uid}".format(uid=uid))
                return 2, self._errno
