import requests
import datetime
import re

from common import security
from urllib import parse
from common.logger import logger

session = 0
host = 0
headers = 0


def get_captcha_code():
    url = "{host}/com_user/weblogin.asp".format(host=host)
    res = session.get(url=url, headers=headers)
    res.encoding = "utf-8"
    captcha_index = res.text.find('placeholder="验证码"')
    return res.text[captcha_index + 30: captcha_index + 34]


def login(uid, password, code):
    url = "{host}/com_user/weblogin.asp".format(host=host)
    data = {
        "username": uid,
        "userpwd": password,
        "code": code,
        "login": "login",
        "checkcode": "1",
        "rank": "0",
        "action": "login",
        "m5": "1",
    }
    res = session.post(url=url, headers=headers, data=data)
    if res.status_code != 200:
        logger.error("POST request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))


def get_id():
    url = "{host}/com_user/left.asp".format(host=host)
    res = session.get(url=url, headers=headers)
    if res.status_code != 200:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    res.encoding = "utf-8"
    try:
        id = re.findall(r"(?<=id=).*?(?=\">我的事务<)", res.text)[0]
        logger.info("Login successfully.")
        logger.info("Get id:{id}.".format(id=id))
        return id
    except Exception as e:
        id = 0
        logger.error("Regular expression match failed.[{e}]".format(e=e))
        logger.error("Login failed.")
        return id


def report(id):
    if id == 0:
        return
    url = "{host}/com_user/project_addx.asp?id={id}&id2={id2}".format(
        host=host, id=id, id2=get_date_url())
    res = session.get(url=url, headers=headers)
    if res.status_code != 200:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))


def get_date_url():
    today = datetime.datetime.now()
    date_ZH = "{y}年{m}月{d}日".format(y=today.year, m=today.month, d=today.day)
    date_url = parse.quote(date_ZH)
    logger.info("Get id2:{id2}.".format(id2=date_url))
    return date_url


def is_reported(id):
    if id == 0:
        return
    url = "{host}/com_user/project.asp?id={id}".format(
        host=host, id=id)
    res = session.get(url=url, headers=headers)
    if res.status_code != 200:
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
        return
    today = datetime.datetime.now()
    today_date = "{y}年{m}月{d}日".format(y=today.year, m=today.month, d=today.day)
    if latest_date == today_date:
        logger.info("Report is existed.")
        return True
    else:
        logger.info("Report is not existed.")
        return False


def main(uid, password):
    global session, host, headers
    session = requests.Session()
    host = "https://xsswzx.cdu.edu.cn/" + security.get_random_host()
    headers = {
        "User-Agent": security.get_random_useragent()
    }
    captcha_code = get_captcha_code()
    login(uid, password, captcha_code)
    id = get_id()
    if is_reported(id):
        logger.info("Report is already existed. ID:{uid}".format(uid=uid))
        return 0
    else:
        report(id)
        if is_reported(id):
            logger.info("Report successfully. ID:{uid}".format(uid=uid))
            return 1
        else:
            logger.error("Report failed. ID:{uid}".format(uid=uid))
            return 2
