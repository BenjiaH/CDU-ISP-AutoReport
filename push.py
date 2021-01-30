import smtplib
import requests

from email.mime.text import MIMEText
from config import global_config
from logger import logger


class Email:
    def __init__(self, mail_user, mail_host, mail_pwd):
        if global_config.getRaw('config', 'email_enable') == 'false':
            return

        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pwd = mail_pwd
        self.is_login = False
        smtpObj = smtplib.SMTP()
        try:
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pwd)
            self.is_login = True
            logger.info("Email login successfully.")
        except Exception as e:
            logger.error("Email login failed.[{e}]".format(e=e))
        self.smtpObj = smtpObj

    def relogin(self):
        smtpObj = smtplib.SMTP()
        try:
            smtpObj.connect(self.mail_host, 25)
            smtpObj.login(self.mail_user, self.mail_pwd)
            self.is_login = True
            logger.info("Email relogin successfully.")
        except Exception as e:
            logger.error("Email relogin failed.[{e}]".format(e=e))
        self.smtpObj = smtpObj

    def send(self, title, msg, receiver: list):
        while True:
            if self.is_login:
                logger.info("Receiver:{receiver}.".format(receiver=receiver[0]))
                message = MIMEText(msg, "plain", "utf-8")
                message['Subject'] = title
                message['From'] = self.mail_user
                message['To'] = receiver[0]
                try:
                    self.smtpObj.sendmail(self.mail_user, receiver, message.as_string())
                    logger.info("Email send successfully.")
                    break
                except Exception as e:
                    logger.error("Email send failed.[{e}]".format(e=e))
                    if str(e) == "please run connect() first":
                        self.is_login = False
                        self.relogin()
            else:
                logger.error("Email not login.")


class Push():
    def __init__(self):
        if global_config.getRaw('config', 'email_enable') == 'true':
            self._bot_email_user = global_config.getRaw('bot_email', 'email_user')
            self._bot_email_host = global_config.getRaw('bot_email', 'email_host')
            self._bot_email_pwd = global_config.getRaw('bot_email', 'email_pwd')
            self.bot_email = Email(self._bot_email_user, self._bot_email_host, self._bot_email_pwd)

    def wechat(self, title, message, sckey):
        url = 'http://sc.ftqq.com/{}.send'.format(sckey)
        payload = {
            "text": title,
            "desp": message
        }
        res = requests.get(url=url, params=payload)
        if res.status_code == 200:
            logger.info("Message send to Wechat successfully. Payload:{payload}. Status code:{code}."
                        .format(payload=payload, code=res.status_code))
        else:
            logger.error("Message send to Wechat failed. Payload:{payload}. Status code:{code}."
                         .format(payload=payload, code=res.status_code))


global_push = Push()
