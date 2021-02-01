import requests
import datetime
import re
import security

from urllib import parse
from time import sleep
from config import global_config
from logger import logger
from push import global_push

session = 0
host = 0
headers = 0


def get_captcha_code():
    url = "{host}/com_user/weblogin.asp".format(host=host)
    res = session.get(url=url, headers=headers)
    res.encoding = "utf-8"
    captcha_index = res.text.find('placeholder="验证码"')
    return (res.text[captcha_index + 30: captcha_index + 34])


def login(studentID, password, code):
    url = "{host}/com_user/weblogin.asp".format(host=host)
    data = {
        "username": studentID,
        "userpwd": password,
        "code": code,
        "login": "login",
        "checkcode": "1",
        "rank": "0",
        "action": "login",
        "m5": "1",
    }
    res = session.post(url=url, headers=headers, data=data)
    if res.status_code == 200:
        logger.info("POST request successfully. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    else:
        logger.error("POST request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))


def get_id(studentID):
    url = "{host}/com_user/left.asp".format(host=host)
    res = session.get(url=url, headers=headers)
    if res.status_code == 200:
        logger.info("GET request successfully. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    else:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    res.encoding = "utf-8"
    try:
        id = re.findall(r"(?<=id=).*?(?=\">我的事务<)", res.text)[0]
        logger.info("Login successfully. ID:{id}.".format(id=studentID))
        return id
    except Exception as e:
        logger.error("Regular expression match failed.[{e}]".format(e=e))
        logger.error("Login failed. ID:{id}.".format(id=studentID))


def report(id):
    if id == None:
        return
    url = "{host}/com_user/project_addx.asp?id={id}&id2={id2}".format(
        host=host, id=id, id2=get_date_url())
    res = session.get(url=url, headers=headers)
    if res.status_code == 200:
        logger.info("GET request successfully. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    else:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    return res.text


def get_date_url():
    today = datetime.datetime.now()
    date_ZH = "{y}年{m}月{d}日".format(y=today.year, m=today.month, d=today.day)
    date_url = parse.quote(date_ZH)
    return date_url


def is_reported(id):
    if id == None:
        return
    url = "{host}/com_user/project.asp?id={id}".format(
        host=host, id=id)
    res = session.get(url=url, headers=headers)
    if res.status_code == 200:
        logger.info("GET request successfully. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    else:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        return
    res.encoding = "utf-8"
    # host refreshes records every months(1st day of this month)
    if "还没有登记记录" in res.text:
        logger.info("Report is not existed.")
        return False
    try:
        latest_date = re.findall(r"(?<=<td class=\"tdmenu\"><div align=\"center\">).*?(?=</div></td>)", res.text)[0]
    except Exception as e:
        logger.error("Regular expression match failed.[{e}]".format(e=e))
    today = datetime.datetime.now()
    date_ZH = "{y}年{m}月{d}日".format(y=today.year, m=today.month, d=today.day)
    if latest_date == date_ZH:
        logger.info("Report is alread existed.")
        return True
    else:
        logger.info("Report is not existed.")
        return False


def main(studentID, password, wechat_push, email_push ,sckey="", email_rever=""):
    global session, host, headers
    session = requests.Session()
    host = security.get_random_host()
    headers = {
        "User-Agent": security.get_random_useragent()
    }
    captcha_code = get_captcha_code()
    login(studentID, password, captcha_code)
    id = get_id(studentID)
    if not is_reported(id):
        report(id)
        if is_reported(id):
            logger.info("Report successfully. ID:{studentID}".format(studentID=studentID))
            title = "打卡成功!"
            message = "{time}打卡成功!学号：{studentID}".format(time=datetime.datetime.now(), studentID=studentID)
            if global_config.getRaw('config', 'wechat_enable') == "true":
                if wechat_push == "1" or wechat_push == "true":
                    global_push.wechat(title, message, sckey)
            if global_config.getRaw('config', 'email_enable') == "true":
                if email_push == "1" or email_push == "true":
                    global_push.bot_email.send(title, message, [email_rever])
        else:
            logger.error("Report failed. ID:{studentID}".format(studentID=studentID))
            title = "打卡失败!"
            message = "{time}打卡失败,请手动打卡!学号：{studentID}".format(time=datetime.datetime.now(), studentID=studentID)
            if global_config.getRaw('config', 'wechat_enable') == "true":
                if wechat_push == "1" or wechat_push == "true":
                    global_push.wechat(title, message, sckey)
            if global_config.getRaw('config', 'email_enable') == "true":
                if email_push == "1" or email_push == "true":
                    global_push.bot_email.send(title, message, [email_rever])
    else:
        logger.info("Report is alread existed. ID:{studentID}".format(studentID=studentID))
        title = "打卡已存在!"
        message = "{time}打卡已存在!学号：{studentID}".format(time=datetime.datetime.now(), studentID=studentID)
        if global_config.getRaw('config', 'wechat_enable') == "true":
            if wechat_push == "1" or wechat_push == "true":
                global_push.wechat(title, message, sckey)
        if global_config.getRaw('config', 'email_enable') == "true":
            if email_push == "1" or email_push == "true":
                global_push.bot_email.send(title, message, [email_rever])
