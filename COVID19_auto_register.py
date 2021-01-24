import requests
import datetime

from urllib import parse
from time import sleep
from config import global_config
from logger import logger

def register():
    url = "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/project_addx.asp?id={id}&id2={id2}".format(id=global_config.getRaw('config', 'id'), id2=get_date_url())
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": global_config.getRaw('config', 'cookie'),
        "Host": "xsswzx.cdu.edu.cn",
        "Referer": "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/project.asp?id={id}".format(id=global_config.getRaw('config', 'id')),
        "Sec-Fetch-Dest": "frame",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50"
    }
    res = requests.get(url=url, headers=headers)
    res.encoding = "utf-8"
    if res.status_code == 200:
        logger.info("register GET request successfully.Status code:{code}".format(code=res.status_code))
    else:
        logger.error("register GET request failed.Status code:{code}".format(code=res.status_code))
    if  "已存在" in res.text:
        logger.info("Register is alread existed.")
        return True, res.text
    else:
        logger.info("Register is not existed.")
        return False, res.text
    # return res.text


def send_wechat(title, message):
    """推送信息到微信"""
    url = 'http://sc.ftqq.com/{}.send'.format(global_config.getRaw('messenger', 'sckey'))
    payload = {
        "text": title,
        "desp": message
    }
    res = requests.get(url, params=payload)
    if res.status_code == 200:
        logger.info("Message send to Wechat successfully. Payload:{payload}. Status code:{code}.".format(payload=payload, code=res.status_code))
    else:
        logger.error("Message send to Wechat failed. Payload:{payload}. Status code:{code}.".format(payload=payload, code=res.status_code))


def get_date_url():
    today = datetime.datetime.now()
    date_ZH = "{y}年{m}月{d}日".format(y=today.year, m=today.month, d=today.day)
    date_url = parse.quote(date_ZH)
    return date_url


def is_register_success():
    result = register()[1]
    # return True
    if  "已存在" in result:
        logger.info("Register successfully.")
        return True
    else:
        logger.info("Register failed.")
        return False


def main():
    if register()[0] == False:
        sleep(2)
        if is_register_success():
            if global_config.getRaw('messenger', 'enable') == 'true':
                message = "{time}打卡成功".format(time=datetime.datetime.now())
                send_wechat("打卡成功", message)
        else:
            if global_config.getRaw('messenger', 'enable') == 'true':
                message = "{time}打卡失败".format(time=datetime.datetime.now())
                send_wechat("打卡失败", message)
    elif register()[0] == True:
        if global_config.getRaw('messenger', 'enable') == 'true':
                message = "{time}打卡已存在".format(time=datetime.datetime.now())
                send_wechat("打卡已存在", message)


if  __name__ == '__main__':
    main()