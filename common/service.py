from datetime import datetime
from time import sleep, time
from common import security
from common.logger import logger
from common.config import global_config
from common.account import global_account
from common.report import Report
from common.push import global_push


class ReportService:
    @logger.catch
    def __init__(self):
        self._str_now_time = "0.1"
        self._wechat_push = global_config.getRaw('config', 'wechat_enable')
        self._email_push = global_config.getRaw('config', 'email_enable')
        self._wechat_type = global_config.getRaw('config', 'wechat_type')
        self._api = global_config.getRaw('config', 'api')
        self._account_cnt = global_account.row
        self._report = Report()

    @logger.catch
    def _get_now_time(self):
        now = datetime.now()
        self._str_now_time = now.strftime("%H.%M")
        return self._str_now_time

    @logger.catch
    def _task(self):
        for i in range(self._account_cnt):
            log_info = f"[{i + 1}/{self._account_cnt}] Report ID:{global_account.studentID(i)}".center(46, '-')
            logger.info(log_info)
            ret = self._report.main(uid=global_account.studentID(i), password=global_account.password(i))
            global_push.push(ret, uid=global_account.studentID(i), wechat_push=global_account.wechat_push(i),
                             email_push=global_account.email_push(i), sendkey=global_account.sendkey(i),
                             email_rxer=global_account.email(i), wechat_type=self._wechat_type,
                             api=self._api, userid=global_account.userid(i))
            sleep(1)

    @logger.catch
    def _gen(self):
        start_time = time()
        if self._account_cnt == 0:
            logger.error("Account does not exist.")
        else:
            security.refresh_hosts()
            global_push.bot_email.login()
            self._report.update_date()
            self._task()
        end_time = time()
        logger.info("Reports are completed. Cost time:{:.2f}s".format(end_time - start_time).center(50, '-'))

    @logger.catch
    def start(self):
        if global_config.getRaw('config', 'timer_enable') == "off":
            logger.info("Timer is disabled.")
            logger.info("Start to report.")
            self._gen()
        else:
            logger.info("Timer is enabled.")
            while True:
                global_config.refresh()
                str_set_time = global_config.getRaw('config', 'set_time')
                str_now_time = self._get_now_time()
                logger.info(f"Now time:{str_now_time}. Set time:{str_set_time}.")
                while True:
                    global_config.refresh()
                    if str_set_time != global_config.getRaw('config', 'set_time'):
                        str_set_time = global_config.getRaw('config', 'set_time')
                        logger.info(f"New set time:{str_set_time}.")
                    str_now_time = self._get_now_time()
                    if str_now_time != str_set_time:
                        # print(str_now_time)
                        sleep(1)
                    else:
                        logger.info("Time arrived. Start to report.")
                        global_account.refresh()
                        self._gen()
                        # avoid running twice in 1 minute
                        logger.info("Cleaning... Estimated:1 min")
                        sleep(60)
                        break
