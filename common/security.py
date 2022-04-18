import random
import requests

from common.logger import logger
from fake_useragent import UserAgent

HOSTS = [
    "ispstu",  # 富强
    "ispstu1-1",  # 民主
    "ispstu1-2",  # 文明
    "ispstu2",  # 和谐
    "ispstu2-1",  # 自由
    "ispstu2-2",  # 平等
    "ispstu3",  # 公正
    "ispstu3-1",  # 法治
    "ispstu3-2",  # 爱国
    "ispstu4",  # 敬业
    "ispstu4-1",  # 诚信
    "ispstu4-3"  # 友善
]
ua = UserAgent(verify_ssl=False)
available_host = []


@logger.catch
def check_host_status(host):
    url = f"https://xsswzx.cdu.edu.cn/{host}/com_user/weblogin.asp"
    try:
        res = requests.get(url=url, timeout=10)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
    except Exception as e:
        logger.error(f'Failed to connect to the server "{host}". [{e}]')
        return False
    res.encoding = "utf-8"
    if "updatenow.asp" in res.text:
        logger.error(f'Failed to connect to the server "{host}". [updating]')
        return False
    elif res.status_code != 200:
        logger.error(f'Failed to connect to the server "{host}". [Status code:{res.status_code}]')
        return False
    else:
        return True


@logger.catch
def refresh_hosts():
    available_host.clear()
    for i in HOSTS:
        if check_host_status(i):
            available_host.append(i)
    logger.info("Successful to refresh hosts status.")
    if len(available_host) == 0:
        logger.error("Available host:[None].")
    elif len(available_host) != len(HOSTS):
        logger.error(f"Available host:{available_host}.")


@logger.catch
def get_random_useragent():
    random_ua = ua.random
    logger.debug(f"User Agent:{random_ua}")
    return random_ua


@logger.catch
def get_random_host():
    try:
        ret_host = random.choice(available_host)
        logger.debug(f'Random host:"{ret_host}".')
    except Exception as e:
        logger.error(e)
        return ""
    return ret_host
