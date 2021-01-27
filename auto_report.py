import requests
import datetime
import re

from urllib import parse
from time import sleep
from config import global_config
from logger import logger

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50",
}


def get_captcha_code():
    url = "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/weblogin.asp"
    res = session.get(url=url, headers=headers)
    res.encoding = "utf-8"
    captcha_index = res.text.find('placeholder="验证码"')
    return (res.text[captcha_index + 30: captcha_index + 34])


def login(studentID, password, code):
    url = "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/weblogin.asp"
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
    return res.text


def get_id():
    url = "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/left.asp"
    res = session.get(url=url, headers=headers)
    if res.status_code == 200:
        logger.info("GET request successfully. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    else:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    res.encoding = "utf-8"
    try:
        id = re.findall(r"(?<=id=).*?(?=\">我的事务<)", res.text)[0]
        return id
    except Exception as e:
        logger.error("Regular expression match failed.[{e}]".format(e=e))


def report(id):
    url = "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/project_addx.asp?id={id}&id2={id2}".format(
        id=id, id2=get_date_url())
    res = session.get(url=url, headers=headers)
    if res.status_code == 200:
        logger.info("GET request successfully. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    else:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    return res.text


def send_wechat(title, message, sckey):
    url = 'http://sc.ftqq.com/{}.send'.format(sckey)
    payload = {
        "text": title,
        "desp": message
    }
    res = requests.get(url=url, params=payload)
    if res.status_code == 200:
        logger.info(
            "Message send to Wechat successfully. Payload:{payload}. Status code:{code}.".format(payload=payload,
                                                                                                 code=res.status_code))
    else:
        logger.error("Message send to Wechat failed. Payload:{payload}. Status code:{code}.".format(payload=payload,
                                                                                                    code=res.status_code))


def get_date_url():
    today = datetime.datetime.now()
    date_ZH = "{y}年{m}月{d}日".format(y=today.year, m=today.month, d=today.day)
    date_url = parse.quote(date_ZH)
    return date_url


def is_reported(id):
    url = "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/project.asp?id={id}".format(
        id=id)
    res = session.get(url=url, headers=headers)
    if res.status_code == 200:
        logger.info("GET request successfully. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    else:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        return
    res.encoding = "utf-8"
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


def main(studentID, password, sckey):
    captcha_code = get_captcha_code()
    login(studentID, password, captcha_code)
    id = get_id()
    if not is_reported(id):
        report(id)
        if is_reported(id):
            logger.info("Report successfully. ID:{studentID}".format(studentID=studentID))
            if global_config.getRaw('messenger', 'enable') == 'true':
                message = "{time}打卡成功!学号：{studentID}".format(time=datetime.datetime.now(), studentID=studentID)
                send_wechat("打卡成功!", message, sckey)
        else:
            logger.error("Report failed. ID:{studentID}".format(studentID=global_config.getRaw('account', 'studentID')))
            if global_config.getRaw('messenger', 'enable') == 'true':
                message = "{time}打卡失败,请手动打卡!学号：{studentID}".format(time=datetime.datetime.now(), studentID=studentID)
                send_wechat("打卡失败!", message, sckey)
    else:
        logger.info("Report is alread existed. ID:{studentID}".format(studentID=studentID))
        if global_config.getRaw('messenger', 'enable') == 'true':
            message = "{time}打卡已存在!学号：{studentID}".format(time=datetime.datetime.now(), studentID=studentID)
            send_wechat("打卡已存在!", message, sckey)
