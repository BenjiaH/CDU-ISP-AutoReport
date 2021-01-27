import datetime

from logger import logger
from config import global_config
from account import global_account
from auto_report import main as ar_main
from time import sleep, time


def main():
    if global_config.getRaw('config', 'timer_enable') != 'true':
        logger.info("Set time mode disable.")
        report_task()
    else:
        str_set_time = global_config.getRaw('config', 'set_time')
        logger.info("Set time mode enable. Set time:{set_time}.".format(set_time=str_set_time))
        logger.info("Waiting...")
        while True:
            now_time = datetime.datetime.now()
            str_now_time = "{h}.{m}".format(h=now_time.hour, m=now_time.minute)
            if str_now_time == str_set_time:
                logger.info("Time arrived. Start to report.")
                report_task()
                sleep(65)
            else:
                # print(str_now_time)
                sleep(1)


def single_mode():
    ar_main(global_config.getRaw('account', 'studentID'), global_config.getRaw('account', 'password'),
            global_config.getRaw('messenger', 'sckey'))


def multiple_mode():
    n = global_account.len
    for i in range(n):
        logger.info("{i}/{n} Reporting... ID:{studentID}.".format(i=i + 1, n=n, studentID=global_account.studentID[i]))
        ar_main(global_account.studentID[i], global_account.password[i], global_account.sckey[i])
        sleep(1.5)


def report_task():
    start_time = time()
    if global_config.getRaw('config', 'multiple_enable') != 'true':
        logger.info("Single account mode.")
        single_mode()
    else:
        logger.info("Multiple account mode.")
        multiple_mode()
    logger.info("Report completed.")
    end_time = time()
    logger.info("Cost time:{:.2f}s.".format(end_time - start_time))


if __name__ == '__main__':
    logger.info("Software started.")
    main()
