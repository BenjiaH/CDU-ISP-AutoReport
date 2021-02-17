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

    def send(self, title, msg, receiver: list):
        while True:
            if self._is_login:
                message = MIMEText(msg, "plain", "utf-8")
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
        self._bot_email_user = global_config.getRaw('bot_email', 'email_user')
        self._bot_email_host = global_config.getRaw('bot_email', 'email_host')
        self._bot_email_pwd = global_config.getRaw('bot_email', 'email_pwd')
        self.bot_email = Email(self._bot_email_user, self._bot_email_host, self._bot_email_pwd)

    @staticmethod
    def wechat(title, message, sckey):
        url = 'http://sc.ftqq.com/{}.send'.format(sckey)
        payload = {
            "text": title,
            "desp": message
        }
        res = requests.get(url=url, params=payload)
        if res.status_code == 200:
            logger.info("Wechat push successfully.")
        else:
            logger.error("Wechat push failed. Status code:{code}.".format(code=res.status_code))


global_push = Push()
