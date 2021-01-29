import smtplib

from email.mime.text import MIMEText
from config import global_config
from logger import logger


class Email():

    def __init__(self, mail_user, mail_host, mail_pwd, ):
        if global_config.getRaw('config', 'email_enable') == 'false':
            return

        smtpObj = smtplib.SMTP()
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.is_login = False
        try:
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pwd)
            self.is_login = True
            logger.info("Email login successfully.")
        except Exception as e:
            logger.error("Email login failed.[{e}]".format(e=e))
        self.smtpObj = smtpObj

    def send(self, title, msg, receiver: list):
        if self.is_login:
            logger.info("Receiver:{receiver}.".format(receiver=receiver[0]))
            message = MIMEText(msg, "plain", "utf-8")
            message['Subject'] = title
            message['From'] = self.mail_user
            message['To'] = receiver[0]
            try:
                self.smtpObj.sendmail(self.mail_user, receiver, message.as_string())
                logger.info("Email send successfully.")
            except Exception as e:
                logger.error("Email send failed.[{e}]".format(e=e))
        else:
            logger.error("Email not login.")


email = Email(
    mail_user=global_config.getRaw('bot_email', 'email_user'),
    mail_host=global_config.getRaw('bot_email', 'email_host'),
    mail_pwd=global_config.getRaw('bot_email', 'email_pwd'),
)
