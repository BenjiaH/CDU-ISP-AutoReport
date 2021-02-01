import datetime
import security

from logger import logger
logger.info("Software started.")
from config import global_config
from time import sleep, time
from account import global_account
from auto_report import main as ar_main


def main():
    if global_config.getRaw('config', 'timer_enable') != 'true':
        logger.info("Set time mode disable.")
        logger.info("Start to report.")
        report_task()
    else:
        while True:
            global_config.refresh()
            str_set_time = global_config.getRaw('config', 'set_time')
            now_time = datetime.datetime.now()
            str_now_time = "{h}.{m}".format(h=now_time.hour, m=now_time.minute)
            logger.info("Set time mode enable. Now_time:{now_time}. Set time:{set_time}."
                        .format(now_time=str_now_time, set_time=str_set_time))
            logger.info("Waiting...")
            while True:
                global_config.refresh()
                if str_set_time != global_config.getRaw('config', 'set_time'):
                    str_set_time = global_config.getRaw('config', 'set_time')
                    logger.info("New set time:{set_time}.".format(set_time=str_set_time))
                    logger.info("Waiting...")
                now_time = datetime.datetime.now()
                str_now_time = "{h}.{m}".format(h=now_time.hour, m=now_time.minute)
                if str_now_time != str_set_time:
                    # print(str_now_time)
                    sleep(1)
                else:
                    logger.info("Time arrived. Start to report.")
                    report_task()
                    # avoid running twice in 1 minute
                    logger.info("Cleaning... Estimated:1min")
                    sleep(60)
                    break


def single_mode():
    ar_main(studentID=global_config.getRaw('account', 'studentID'), password=global_config.getRaw('account', 'password'),
            wechat_push=global_config.getRaw('config', 'wechat_enable'), email_push=global_config.getRaw('config', 'email_enable'), 
            sckey=global_config.getRaw('messenger', 'sckey'),email_rever=global_config.getRaw('messenger', 'email'))


def multiple_mode():
    global_account.refresh()
    n = global_account.row
    for i in range(n):
        logger.info("{i}/{n} Reporting... ID:{studentID}.".format(i=i + 1, n=n, studentID=global_account.studentID[i]))
        ar_main(studentID = global_account.studentID[i], password=global_account.password[i],
                wechat_push=global_account.wechat_push[i], email_push=global_account.email_push[i],
                sckey=global_account.sckey[i],email_rever=global_account.email[i])
        sleep(1.5)


def report_task():
    start_time = time()
    security.refresh_hosts()
    if global_config.getRaw('config', 'multiple_enable') != 'true':
        logger.info("Single account mode.")
        single_mode()
    else:
        logger.info("Multiple account mode.")
        multiple_mode()
    end_time = time()
    logger.info("Report completed. Cost time:{:.2f}s.".format(end_time - start_time))


if __name__ == '__main__':
    main()
