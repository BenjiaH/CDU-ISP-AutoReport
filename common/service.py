from datetime import datetime
from time import sleep, time
from common.utils import utils
from common.logger import logger
from common.config import config
from common.account import global_account
from common.report import report
from common.push import push


class ReportService:
    @logger.catch
    def __init__(self):
        self._str_now_time = "0.1"
        self._account_cnt = global_account.row
        self._wechat_push = None
        self._wechat_type = None
        self._api = None
        self._email_push = None
        self._timer_switch = None
        self.fetch_param()

    @logger.catch
    def fetch_param(self):
        self._wechat_push = config.config('/setting/push/wechat/switch', utils.get_call_loc())
        self._wechat_type = config.config('/setting/push/wechat/type', utils.get_call_loc())
        self._api = config.config('/setting/push/wechat/api', utils.get_call_loc())
        self._email_push = config.config('/setting/push/email/switch', utils.get_call_loc())
        self._timer_switch = config.config('/setting/timer/switch', utils.get_call_loc())
        logger.debug("Fetched [ReportService] params.")

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
            ret = report.main(uid=global_account.studentID(i), password=global_account.password(i))
            push.push(ret, uid=global_account.studentID(i), wechat_push=global_account.wechat_push(i),
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
            utils.refresh_hosts()
            push.bot_email.login()
            utils.update_date()
            self._task()
        end_time = time()
        cost = f"{(end_time - start_time):.2f}"
        logger.info(f"Reports are completed. Cost time:{cost}s".center(50, '-'))

    @logger.catch
    def start(self):
        if self._timer_switch == "off":
            logger.info("Timer is disabled.")
            logger.info("Start to report.")
            self._gen()
        else:
            logger.info("Timer is enabled.")
            while True:
                config.refresh()
                str_set_time = str(config.config('/setting/timer/set_time', utils.get_call_loc()))
                str_now_time = self._get_now_time()
                logger.info(f"Now time:{str_now_time}. Set time:{str_set_time}.")
                while True:
                    config.refresh()
                    if str_set_time != str(config.config('/setting/timer/set_time', utils.get_call_loc())):
                        str_set_time = str(config.config('/setting/timer/set_time', utils.get_call_loc()))
                        logger.info(f"New set time:{str_set_time}.")
                    str_now_time = self._get_now_time()
                    if str_now_time != str_set_time:
                        # print(str_now_time)
                        sleep(1)
                    else:
                        logger.info("Time arrived. Start to report.")
                        global_account.refresh()
                        utils.refresh_param()
                        self._gen()
                        # avoid running twice in 1 minute
                        logger.info("Cleaning... Estimated:1 min")
                        sleep(60)
                        break


report_service = ReportService()
