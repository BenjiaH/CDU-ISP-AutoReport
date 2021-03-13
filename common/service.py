from datetime import datetime
from time import sleep, time
from common import security
from common.logger import logger
from common.config import global_config
from common.account import global_account
from common.report import Report
from common.push import global_push


class ReportService:
    def __init__(self):
        self._str_now_time = "0.1"
        self._global_wechat = global_config.getRaw('config', 'wechat_enable')
        self._global_email = global_config.getRaw('config', 'email_enable')
        self._uid = global_config.getRaw('account', 'studentID')
        self._password = global_config.getRaw('account', 'password')
        self._wechat_push = global_config.getRaw('config', 'wechat_enable')
        self._email_push = global_config.getRaw('config', 'email_enable')
        self._sckey = global_config.getRaw('messenger', 'sckey')
        self._email_rxer = global_config.getRaw('messenger', 'email')
        self._report = Report()

    def _get_now_time(self):
        now = datetime.now()
        self._str_now_time = now.strftime("%H.%M")
        return self._str_now_time

    def _single_mode(self):
        logger.info("Report ID:{studentID}.".format(studentID=self._uid))
        ret = self._report.main(uid=self._uid, password=self._password)
        global_push.push(ret, uid=self._uid, wechat_push=self._wechat_push, email_push=self._email_push,
                         sckey=self._sckey, email_rxer=self._email_rxer)

    def _multiple_mode(self):
        global_account.refresh()
        n = global_account.row
        for i in range(n):
            logger.info(
                "{i}/{n} Report ID:{studentID}.".format(i=i + 1, n=n, studentID=global_account.studentID[i]))
            ret = self._report.main(uid=global_account.studentID[i], password=global_account.password[i])
            global_push.push(ret, uid=global_account.studentID[i], wechat_push=global_account.wechat_push[i],
                             email_push=global_account.email_push[i], sckey=global_account.sckey[i],
                             email_rxer=global_account.email[i])
            sleep(1.5)

    def _gen(self):
        start_time = time()
        security.refresh_hosts()
        global_push.bot_email.login()
        self._report.update_date()
        if global_config.getRaw('config', 'multiple_enable') == "off":
            logger.info("Single account mode.")
            self._single_mode()
        else:
            logger.info("Multiple account mode.")
            self._multiple_mode()
        end_time = time()
        logger.info("Report completed. Cost time:{:.2f}s.".format(end_time - start_time))

    def start(self):
        if global_config.getRaw('config', 'timer_enable') == "off":
            logger.info("Timer disabled.")
            logger.info("Start to report.")
            self._gen()
        else:
            while True:
                global_config.refresh()
                str_set_time = global_config.getRaw('config', 'set_time')
                str_now_time = self._get_now_time()
                logger.info("Timer enabled.")
                logger.info(
                    "Now time:{now_time}. Set time:{set_time}.".format(now_time=str_now_time, set_time=str_set_time))
                while True:
                    global_config.refresh()
                    if str_set_time != global_config.getRaw('config', 'set_time'):
                        str_set_time = global_config.getRaw('config', 'set_time')
                        logger.info("New set time:{set_time}.".format(set_time=str_set_time))
                    str_now_time = self._get_now_time()
                    if str_now_time != str_set_time:
                        # print(str_now_time)
                        sleep(1)
                    else:
                        logger.info("Time arrived. Start to report.")
                        self._gen()
                        # avoid running twice in 1 minute
                        logger.info("Cleaning... Estimated:1min")
                        sleep(60)
                        break
