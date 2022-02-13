import random
import requests

from common.logger import logger
from fake_useragent import UserAgent

HOSTS = [
    "ispteacher/teacher_admin5"  # 教师入口
]
ua = UserAgent(verify_ssl=False)
available_host = []


@logger.catch
def get_host_status(host):
    url = f"https://xsswzx.cdu.edu.cn/{host}/weblogin.asp"
    try:
        res = requests.get(url=url, timeout=10)
        logger.debug(f"URL:{url}. Status code:{res.status_code}")
    except Exception as e:
        logger.error(f'Failed to check "{host}" status.')
        logger.debug(f'Failed to check "{host}" status. [{e}]')
        return False
    res.encoding = "utf-8"
    if "updatenow.asp" in res.text:
        logger.error(f'Failed to check "{host}" status.')
        logger.debug(f'Failed to check "{host}" status. [updating]')
        return False
    elif res.status_code != 200:
        logger.error(f'Failed to check "{host}" status.')
        logger.debug(f'Failed to check "{host}" status. [Status code:{res.status_code}]')
        return False
    else:
        return True


@logger.catch
def refresh_hosts():
    available_host.clear()
    for i in HOSTS:
        if get_host_status(i):
            available_host.append(i)
    logger.info("Successful to refresh hosts status.")
    if len(available_host) != len(HOSTS):
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
