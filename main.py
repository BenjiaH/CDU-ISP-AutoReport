import datetime
import security

from logger import logger
from config import global_config
from time import sleep, time
from account import global_account
from auto_report import main as ar_main
from push import global_push


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
    logger.info("Reporting... ID:{studentID}.".format(studentID=global_config.getRaw('account', 'studentID')))
    ret = ar_main(uid=global_config.getRaw('account', 'studentID'),
                  password=global_config.getRaw('account', 'password'))
    push(ret, uid=global_config.getRaw('account', 'studentID'),
         wechat_push=global_config.getRaw('config', 'wechat_enable'),
         email_push=global_config.getRaw('config', 'email_enable'), sckey=global_config.getRaw('messenger', 'sckey'),
         email_rxer=global_config.getRaw('messenger', 'email'))


def multiple_mode():
    global_account.refresh()
    n = global_account.row
    for i in range(n):
        logger.info("{i}/{n} Reporting... ID:{studentID}.".format(i=i + 1, n=n, studentID=global_account.studentID[i]))
        ret = ar_main(uid=global_account.studentID[i], password=global_account.password[i])
        push(ret, uid=global_account.studentID[i], wechat_push=global_account.wechat_push[i],
             email_push=global_account.email_push[i], sckey=global_account.sckey[i],
             email_rxer=global_account.email[i])
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


def push(result, uid, wechat_push, email_push, sckey="", email_rxer=""):
    pass
    global_wechat = global_config.getRaw('config', 'wechat_enable')
    global_email = global_config.getRaw('config', 'email_enable')
    if result == 0:
        title = "打卡已存在!"
        message = "{time}打卡已存在!学号：{uid}".format(time=datetime.datetime.now(), uid=uid)
        if global_wechat == "true":
            if wechat_push == "1" or wechat_push == "true":
                global_push.wechat(title, message, sckey)
        if global_email == "true":
            if email_push == "1" or email_push == "true":
                global_push.bot_email.send(title, message, [email_rxer])
    elif result == 1:
        title = "打卡成功!"
        message = "{time}打卡成功!学号：{uid}".format(time=datetime.datetime.now(), uid=uid)
        if global_wechat == "true":
            if wechat_push == "1" or wechat_push == "true":
                global_push.wechat(title, message, sckey)
        if global_email == "true":
            if email_push == "1" or email_push == "true":
                global_push.bot_email.send(title, message, [email_rxer])
    elif result == 2:
        title = "打卡失败!"
        message = "{time}打卡失败,请手动打卡!学号：{uid}".format(time=datetime.datetime.now(), uid=uid)
        if global_wechat == "true":
            if wechat_push == "1" or wechat_push == "true":
                global_push.wechat(title, message, sckey)
        if global_email == "true":
            if email_push == "1" or email_push == "true":
                global_push.bot_email.send(title, message, [email_rxer])


if __name__ == '__main__':
    main()
