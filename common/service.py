import datetime

from time import sleep, time
from common import security
from common.logger import logger
from common.config import global_config
from common.account import global_account
from common.report import main as ar_main
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

    def _get_now_time(self):
        now_time = datetime.datetime.now()
        self._str_now_time = "{h}.{m}".format(h=now_time.hour, m=now_time.minute)
        return self._str_now_time

    def _single_mode(self):
        logger.info("Report ID:{studentID}.".format(studentID=self._uid))
        ret = ar_main(uid=self._uid, password=self._password)
        self._push(ret, uid=self._uid, wechat_push=self._wechat_push, email_push=self._email_push, sckey=self._sckey,
                   email_rxer=self._email_rxer)

    def _multiple_mode(self):
        global_account.refresh()
        n = global_account.row
        for i in range(n):
            logger.info(
                "{i}/{n} Report ID:{studentID}.".format(i=i + 1, n=n, studentID=global_account.studentID[i]))
            ret = ar_main(uid=global_account.studentID[i], password=global_account.password[i])
            self._push(ret, uid=global_account.studentID[i], wechat_push=global_account.wechat_push[i],
                       email_push=global_account.email_push[i], sckey=global_account.sckey[i],
                       email_rxer=global_account.email[i])
            sleep(1.5)

    def _gen(self):
        start_time = time()
        security.refresh_hosts()
        global_push.bot_email.login()
        if global_config.getRaw('config', 'multiple_enable') != 'true':
            logger.info("Single account mode.")
            self._single_mode()
        else:
            logger.info("Multiple account mode.")
            self._multiple_mode()
        end_time = time()
        logger.info("Report completed. Cost time:{:.2f}s.".format(end_time - start_time))

    def _push(self, result, uid, wechat_push, email_push, sckey="", email_rxer=""):
        if result == 0:
            title = "打卡已存在!"
            message = "{time}打卡已存在!学号：{uid}".format(time=datetime.datetime.now(), uid=uid)
        elif result == 1:
            title = "打卡成功!"
            message = "{time}打卡成功!学号：{uid}".format(time=datetime.datetime.now(), uid=uid)
        elif result == 2:
            title = "打卡失败!"
            message = "{time}打卡失败,请手动打卡!学号：{uid}".format(time=datetime.datetime.now(), uid=uid)
        else:
            title = "ERROR!"
            message = "{time}ERROR!学号：{uid}".format(time=datetime.datetime.now(), uid=uid)
        if self._global_wechat == "true":
            if wechat_push == "1" or wechat_push == "true":
                global_push.wechat(title, message, sckey)
        if self._global_email == "true":
            if email_push == "1" or email_push == "true":
                global_push.bot_email.send(title, message, [email_rxer])

    def start(self):
        if global_config.getRaw('config', 'timer_enable') != 'true':
            logger.info("Set time mode disable.")
            logger.info("Start to report.")
            self._gen()
        else:
            while True:
                global_config.refresh()
                str_set_time = global_config.getRaw('config', 'set_time')
                str_now_time = self._get_now_time()
                logger.info("Set time mode enable.")
                logger.info(
                    "Now time:{now_time}. Set time:{set_time}.".format(now_time=str_now_time, set_time=str_set_time))
                logger.info("Waiting...")
                while True:
                    global_config.refresh()
                    if str_set_time != global_config.getRaw('config', 'set_time'):
                        str_set_time = global_config.getRaw('config', 'set_time')
                        logger.info("New set time:{set_time}.".format(set_time=str_set_time))
                        logger.info("Waiting...")
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


report_service = ReportService()
