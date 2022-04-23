import random
import requests

from common.logger import logger
from common.config import global_config as gc
from fake_useragent import UserAgent

HOSTS = list(gc.config['config']['all_hosts'].keys())
ua = UserAgent(verify_ssl=False)
available_host = []


@logger.catch
def check_host_status(host):
    url_0 = gc.config['config']['url']['host_head']
    url_1 = host
    url_2 = gc.config['config']['url']['host_foot']
    url_3 = gc.config['config']['url']['login']
    url = f"{url_0}/{url_1}/{url_2}/{url_3}"
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
    logger.info("Successful to check hosts status.")
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
