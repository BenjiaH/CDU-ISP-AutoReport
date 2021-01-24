import requests
import datetime
import re

from urllib import parse
from time import sleep
from config import global_config
from logger import logger


def register():
    url = "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/project_addx.asp?id={id}&id2={id2}".format(
        id=global_config.getRaw('config', 'id'), id2=get_date_url())
    headers = {
        "Cookie": global_config.getRaw('config', 'cookie'),
        "Referer": "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/project.asp?id={id}".format(
            id=global_config.getRaw('config', 'id')),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50"
    }
    res = requests.get(url=url, headers=headers)
    res.encoding = "utf-8"
    if res.status_code == 200:
        logger.info("GET request successfully. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    else:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    return res.text


def send_wechat(title, message):
    """推送信息到微信"""
    url = 'http://sc.ftqq.com/{}.send'.format(global_config.getRaw('messenger', 'sckey'))
    payload = {
        "text": title,
        "desp": message
    }
    res = requests.get(url, params=payload)
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


def is_registered():
    url = "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/project.asp?id={id}".format(
        id=global_config.getRaw('config', 'id'))
    headers = {
        "Cookie": global_config.getRaw('config', 'cookie'),
        "Referer": "https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/left.asp",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50"
    }
    res = requests.get(url=url, headers=headers)
    res.encoding = "utf-8"
    if res.status_code == 200:
        logger.info("GET request successfully. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
    else:
        logger.error("GET request failed. URL:{url}. Status code:{code}".format(url=url, code=res.status_code))
        return
    latest_date = re.findall(r"(?<=<td class=\"tdmenu\"><div align=\"center\">).*?(?=</div></td>)", res.text)[0]
    today = datetime.datetime.now()
    date_ZH = "{y}年{m}月{d}日".format(y=today.year, m=today.month, d=today.day)
    print(latest_date, date_ZH)
    if latest_date == date_ZH:
        logger.info("Register is alread existed.")
        return True
    else:
        logger.info("Register is not existed.")
        return False


def main():
    if not is_registered():
        register()
        if is_registered():
            if global_config.getRaw('messenger', 'enable') == 'true':
                message = "{time}打卡成功".format(time=datetime.datetime.now())
                send_wechat("打卡成功", message)
        else:
            if global_config.getRaw('messenger', 'enable') == 'true':
                message = "{time}打卡失败".format(time=datetime.datetime.now())
                send_wechat("打卡失败", message)
    else:
        if global_config.getRaw('messenger', 'enable') == 'true':
            message = "{time}打卡已存在".format(time=datetime.datetime.now())
            send_wechat("打卡已存在", message)


if __name__ == '__main__':
    main()
