import random
import requests
import copy

from common.logger import logger
from fake_useragent import UserAgent

HOSTS = [
    "ispteacher/teacher_admin5"  # 教师入口
]
ua = UserAgent(verify_ssl=False)
# deep copy
hosts = copy.deepcopy(HOSTS)


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
    global hosts
    unavailable_host = []
    # deep copy
    hosts = copy.deepcopy(HOSTS)
    for i in hosts:
        if not get_host_status(i):
            hosts.remove(i)
            unavailable_host.append(i)
    logger.info("Successful to refresh hosts status.")
    if len(hosts) != len(HOSTS):
        logger.error(f"Unavailable host:{unavailable_host}.")
    unavailable_host.clear()
    return hosts


@logger.catch
def get_random_useragent():
    random_ua = ua.random
    logger.debug(f"User Agent:{random_ua}")
    return random_ua


@logger.catch
def get_random_host():
    try:
        ret_host = random.choice(hosts)
        logger.debug(f'Random host:"{ret_host}".')
    except Exception as e:
        logger.error(f"{e}.")
        return ""
    return ret_host
