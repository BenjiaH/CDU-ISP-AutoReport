import json
import smtplib
import requests
import os

from retrying import retry
from urllib import parse
from datetime import datetime
from email.mime.text import MIMEText
from common.config import global_config as gc
from common.logger import logger


class Email:
    @logger.catch
    def __init__(self, mail_user, mail_host, mail_pwd):
        if gc.config['setting']['push']['email']['enable'] == "off":
            logger.debug("Email is disabled")
            return
        logger.debug("Email is enabled")
        self._mail_host = mail_host
        self._mail_user = mail_user
        self._mail_name = self._mail_user.split("@")[0]
        self._mail_pwd = mail_pwd
        self._is_login = False
        self.smtp = 0
        self._mail_payload = ""
        self._email_tmpl_path = gc.config['config']['path']['email_tmpl']

    @logger.catch
    def _load_tmpl(self):
        os.chdir(os.path.dirname(__file__))
        with open(self._email_tmpl_path, "r", encoding="utf-8") as f:
            self._mail_payload = f.read()
            logger.debug(f'Loaded [{os.path.abspath(r"../res/email_tmpl.html")}]')

    @logger.catch
    def login(self):
        if gc.config['setting']['push']['email']['enable'] == "off":
            return
        self._load_tmpl()
        try:
            smtp = smtplib.SMTP_SSL(self._mail_host, 465, timeout=20)
            smtp.login(self._mail_user, self._mail_pwd)
            self._is_login = True
            logger.info("Successful to login the email.")
        except Exception as e:
            logger.error(f"Failed to login the email. [{e}]")
        self.smtp = smtp

    @retry(stop_max_attempt_number=3, wait_fixed=500)
    def send(self, uid, title, msg, receiver: list):
        logger.debug(f"Email receiver:{receiver[0]}.")
        if not self._is_login:
            logger.error("Failed to send the email.[Email not login]")
            self.login()
            raise Exception("Failed to send the email.")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mail_msg = self._mail_payload.format(uid=uid, msg=msg, mail_name=self._mail_name, time=now)
            message = MIMEText(mail_msg, "html", "utf-8")
            message['Subject'] = title
            message['From'] = f"{self._mail_name} <{self._mail_user}>"
            message['To'] = receiver[0]
            try:
                self.smtp.sendmail(self._mail_user, receiver, message.as_string())
                logger.info("Successful to send the email.")
            except Exception as e:
                logger.error(f"Failed to send the email.[{e}]")
                logger.error("Retry to send the email.")
                self._is_login = False
                self.login()
                raise Exception("Failed to send the email.")


class Push:
    @logger.catch
    def __init__(self):
        self._global_wechat = gc.config['setting']['push']['wechat']['enable']
        self._global_email = gc.config['setting']['push']['email']['enable']
        self._bot_email_user = gc.config['bot_email']['email_user']
        self._bot_email_host = gc.config['bot_email']['email_host']
        self._bot_email_pwd = gc.config['bot_email']['email_pwd']
        self.bot_email = Email(self._bot_email_user, self._bot_email_host, self._bot_email_pwd)
        self._errno_msg = gc.config['config']['errmsg']

    @staticmethod
    @logger.catch
    def sct_wechat(uid, title, message, sendkey):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = f"{gc.config['config']['url']['sct']}/{sendkey}.send"
        ps = ""
        msg = f'{" " * 10}{title}\n\n{uid}:\n{" " * 4}{message}\n{ps}\n\n{now}'
        payload = {
            "title": title,
            "desp": parse.quote(msg)
        }
        res = requests.get(url=url, params=payload)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        logger.debug(f"Response:{res.text}")
        if res.status_code != 200:
            logger.error(f"Failed to push the WeChat message. Status code:{res.status_code}.")
            return False
        else:
            logger.info("Successful to push the WeChat message.")
            return True

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_fixed=500)
    def go_scf_wechat(uid, title, message, api, sendkey, userid):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = f'{api}/{sendkey}'
        ps = ""
        msg = f'{" " * 10}{title}\n\n{uid}:\n{" " * 4}{message}\n{ps}\n\n{now}'
        payload = {
            "sendkey": sendkey,
            "msg_type": "text",
            "msg": msg,
            "to_user": userid
        }
        # go_scf post请求body必须为json
        # 详见文档:https://github.com/riba2534/wecomchan/tree/main/go-scf#%E4%BD%BF%E7%94%A8-post-%E8%BF%9B%E8%A1%8C%E8%AF%B7%E6%B1%82
        res = requests.post(url=url, data=json.dumps(payload))
        payload["sendkey"] = "*******"
        logger.debug(f"URL:{url}. Payload:{payload}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        logger.debug(f"Response:{res.text}")
        dict_res = json.loads(res.text)
        if res.status_code != 200:
            logger.error(f"Failed to push the WeChat message. Status code:{res.status_code}.")
            logger.error("Retry to push the WeChat message.")
            raise Exception("Failed to push the WeChat message.")
        elif dict_res["code"] != 0:
            logger.error(f'Failed to push the WeChat message. [{dict_res["msg"]}].')
            logger.error("Retry to push the WeChat message.")
            raise Exception("Failed to push the WeChat message.")
        else:
            logger.info("Successful to push the WeChat message.")

    @logger.catch
    def push(self, result, uid, wechat_push, email_push, wechat_type, api, userid, sendkey="", email_rxer=""):
        status = result[0]
        errno = result[1]
        if status == 0:
            title = "[打卡已存在]"
            message = "当日打卡已存在!"
        elif status == 1:
            title = "[打卡成功]"
            message = "打卡成功!"
        elif status == 2:
            title = "[打卡失败]"
            message = "打卡可能失败,请手动打卡!"
        else:
            title = "[ERROR]"
            message = "ERROR!"
        if errno != 0:
            errmsg = [i["msg"] for i in self._errno_msg if errno == i["errno"]][0]
            message = f'{message}[错误信息:"{errmsg}"]'
        logger.debug(f"Title:{title}#Message:{message}#Error code:{errno}")
        if self._global_wechat != "off":
            if wechat_push == "1":
                try:
                    if str(wechat_type) == "1":
                        self.sct_wechat(uid, title, message, sendkey)
                    else:
                        self.go_scf_wechat(uid, title, message, api, sendkey, userid)
                except Exception as e:
                    logger.error(e)
        if self._global_email != "off":
            if email_push == "1":
                try:
                    self.bot_email.send(uid, title, message, [email_rxer])
                except Exception as e:
                    logger.error(e)


global_push = Push()
