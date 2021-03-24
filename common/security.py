import random
import requests
import copy

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
# deep copy
hosts = copy.deepcopy(HOSTS)


@logger.catch
def get_host_status(host):
    url = "https://xsswzx.cdu.edu.cn/{host}/com_user/weblogin.asp".format(host=host)
    try:
        res = requests.get(url=url, timeout=5)
    except Exception as e:
        logger.error("Check \"{host}\" status failed. [{e}]".format(host=host, e=e))
        return False
    res.encoding = "utf-8"
    if "updatenow.asp" in res.text:
        logger.error("Check \"{host}\" status failed. [updating]".format(host=host))
        return False
    elif res.status_code != 200:
        logger.error("Check \"{host}\" status failed. [status code:{code}]".format(host=host, code=res.status_code))
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
    logger.info("Hosts refreshed.")
    if len(hosts) != len(HOSTS):
        logger.error("Unavailable host:{host}.".format(host=unavailable_host))
    unavailable_host.clear()
    return hosts


@logger.catch
def get_random_useragent():
    return ua.random


@logger.catch
def get_random_host():
    try:
        ret_host = random.choice(hosts)
        logger.info("Random host:\"{ret_host}\".".format(ret_host=ret_host))
    except Exception as e:
        logger.error("{e}.".format(e=e))
        return ""
    return ret_host
