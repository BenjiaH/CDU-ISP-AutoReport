import json
import smtplib
import requests
import os

from datetime import datetime
from email.mime.text import MIMEText
from common.config import global_config
from common.logger import logger


class Email:
    @logger.catch
    def __init__(self, mail_user, mail_host, mail_pwd):
        if global_config.getRaw('config', 'email_enable') == "off":
            logger.debug("Email disabled")
            return

        self._mail_host = mail_host
        self._mail_user = mail_user
        self._mail_name = self._mail_user.split("@")[0]
        self._mail_pwd = mail_pwd
        self._is_login = False
        self.smtp = 0
        self._mail_payload = ""

    @logger.catch
    def _load_tmpl(self):
        os.chdir(os.path.dirname(__file__))
        with open(r"../res/email_tmpl.html", "r", encoding="UTF-8") as f:
            self._mail_payload = f.read()
            logger.debug("Loaded:{tmpl}.".format(tmpl=os.path.abspath(r"../res/email_tmpl.html")))

    @logger.catch
    def login(self):
        if global_config.getRaw('config', 'email_enable') == "off":
            return
        self._load_tmpl()
        smtp = smtplib.SMTP(timeout=20)
        try:
            smtp.connect(self._mail_host, 25)
            smtp.login(self._mail_user, self._mail_pwd)
            self._is_login = True
            logger.info("Email login successfully.")
        except Exception as e:
            logger.error("Email login failed.[{e}]".format(e=e))
        self.smtp = smtp

    @logger.catch
    def send(self, uid, title, msg, receiver: list):
        logger.debug("Email receiver:{rxer}.".format(rxer=receiver[0]))
        if not self._is_login:
            logger.error("Email send failed.[Email not login]")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mail_msg = self._mail_payload.format(uid=uid, msg=msg, mail_name=self._mail_name, time=now)
            message = MIMEText(mail_msg, "html", "utf-8")
            message['Subject'] = title
            message['From'] = "{mail_name} <{mail_user}>".format(mail_name=self._mail_name,
                                                                 mail_user=self._mail_user)
            message['To'] = receiver[0]
            try:
                self.smtp.sendmail(self._mail_user, receiver, message.as_string())
                logger.info("Email send successfully.")
            except Exception as e:
                logger.error("Email send failed.[{e}]".format(e=e))
                error_msg = ["please run connect() first", "Connection unexpectedly closed"]
                if str(e) in error_msg:
                    self._is_login = False
                    self.login()


class Push:
    @logger.catch
    def __init__(self):
        self._global_wechat = global_config.getRaw('config', 'wechat_enable')
        self._global_email = global_config.getRaw('config', 'email_enable')
        self._bot_email_user = global_config.getRaw('bot_email', 'email_user')
        self._bot_email_host = global_config.getRaw('bot_email', 'email_host')
        self._bot_email_pwd = global_config.getRaw('bot_email', 'email_pwd')
        self.bot_email = Email(self._bot_email_user, self._bot_email_host, self._bot_email_pwd)

    @staticmethod
    @logger.catch
    def wechat(uid, title, message, sckey):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = 'http://sc.ftqq.com/{}.send'.format(sckey)
        payload = {
            "text": title,
            "desp": uid + ":\n\n" + message + "\n\n`{time}`".format(time=now)
        }
        res = requests.get(url=url, params=payload)
        res.encoding = "utf-8"
        dict_res = json.loads(res.text)
        logger.debug("URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        logger.debug("Response:{res}".format(res=dict_res))
        if res.status_code != 200:
            logger.error("Wechat push failed. Status code:{code}.".format(code=res.status_code))
            return False
        elif dict_res["errno"] != 0:
            logger.error("Wechat push failed. [{msg}].".format(msg=dict_res["errmsg"]))
            return False
        else:
            logger.info("Wechat push successfully.")
            return True

    @logger.catch
    def push(self, result, uid, wechat_push, email_push, sckey="", email_rxer=""):
        if result == 0:
            title = "打卡已存在!"
            message = "当日打卡已存在!"
        elif result == 1:
            title = "打卡成功!"
            message = "打卡成功!"
        elif result == 2:
            title = "打卡失败!"
            message = "打卡失败,请手动打卡!"
        else:
            title = "ERROR!"
            message = "ERROR!"
        if self._global_wechat != "off":
            if wechat_push == "1" or wechat_push == "on":
                self.wechat(uid, title, message, sckey)
        if self._global_email != "off":
            if email_push == "1" or email_push == "on":
                self.bot_email.send(uid, title, message, [email_rxer])


global_push = Push()
