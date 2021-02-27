import datetime
import json
import smtplib
import requests

from email.mime.text import MIMEText
from common.config import global_config
from common.logger import logger


class Email:
    def __init__(self, mail_user, mail_host, mail_pwd):
        if global_config.getRaw('config', 'email_enable') == 'false':
            return

        self._mail_host = mail_host
        self._mail_user = mail_user
        self._mail_pwd = mail_pwd
        self._is_login = False
        self.smtp = 0

    def login(self):
        if global_config.getRaw('config', 'email_enable') == 'false':
            return
        smtp = smtplib.SMTP()
        try:
            smtp.connect(self._mail_host, 25)
            smtp.login(self._mail_user, self._mail_pwd)
            self._is_login = True
            logger.info("Email login successfully.")
        except Exception as e:
            logger.error("Email login failed.[{e}]".format(e=e))
        self.smtp = smtp

    def send(self, uid, title, msg, time, receiver: list):
        while True:
            if self._is_login:
                # message = MIMEText(msg, "plain", "utf-8")
                mail_msg = """
                {uid}:
                <p style="text-indent:2em">
                    {msg}</p>
                <br>
                <p align="right">autoreport_bot</p>
                <p align="right">{time}</p>
                """.format(uid=uid, msg=msg, time=time)
                message = MIMEText(mail_msg, "html", "utf-8")
                message['Subject'] = title
                message['From'] = self._mail_user
                message['To'] = receiver[0]
                try:
                    self.smtp.sendmail(self._mail_user, receiver, message.as_string())
                    logger.info("Email send successfully.")
                    break
                except Exception as e:
                    logger.error("Email send failed.[{e}]".format(e=e))
                    error_msg = ["please run connect() first", "Connection unexpectedly closed"]
                    if str(e) in error_msg:
                        self._is_login = False
                        self.login()
                    else:
                        return
            else:
                logger.error("Email not login.")


class Push:
    def __init__(self):
        self._global_wechat = global_config.getRaw('config', 'wechat_enable')
        self._global_email = global_config.getRaw('config', 'email_enable')
        self._bot_email_user = global_config.getRaw('bot_email', 'email_user')
        self._bot_email_host = global_config.getRaw('bot_email', 'email_host')
        self._bot_email_pwd = global_config.getRaw('bot_email', 'email_pwd')
        self.bot_email = Email(self._bot_email_user, self._bot_email_host, self._bot_email_pwd)

    @staticmethod
    def wechat(uid, title, message, time, sckey):
        url = 'http://sc.ftqq.com/{}.send'.format(sckey)
        payload = {
            "text": title,
            "desp": uid + ":\n\n" + message + "\n\n`{time}`".format(time=time)
        }
        res = requests.get(url=url, params=payload)
        res.encoding = "utf-8"
        dict_res = json.loads(res.text)
        if res.status_code != 200:
            logger.error("Wechat push failed. Status code:{code}.".format(code=res.status_code))
            return False
        elif dict_res["errno"] != 0:
            logger.error("Wechat push failed. [{msg}].".format(msg=dict_res["errmsg"]))
            return False
        else:
            logger.info("Wechat push successfully.")
            return True

    def push(self, result, uid, wechat_push, email_push, sckey="", email_rxer=""):
        now_time = datetime.datetime.now()
        if result == 0:
            title = "打卡已存在!"
            # message = "{time}打卡已存在!学号：{uid}".format(time=now_time, uid=uid)
            message = "当日打卡已存在!"
        elif result == 1:
            title = "打卡成功!"
            # message = "{time}打卡成功!学号：{uid}".format(time=now_time, uid=uid)
            message = "打卡成功!"
        elif result == 2:
            title = "打卡失败!"
            # message = "{time}打卡失败,请手动打卡!学号：{uid}".format(time=now_time, uid=uid)
            message = "打卡失败,请手动打卡!"
        else:
            title = "ERROR!"
            # message = "{time}ERROR!学号：{uid}".format(time=now_time, uid=uid)
            message = "ERROR!"
        if self._global_wechat == "true":
            if wechat_push == "1" or wechat_push == "true":
                self.wechat(uid, title, message, now_time, sckey)
        if self._global_email == "true":
            if email_push == "1" or email_push == "true":
                self.bot_email.send(uid, title, message, now_time, [email_rxer])


global_push = Push()
