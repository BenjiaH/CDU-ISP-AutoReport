import datetime

from logger import logger
from config import global_config
from COVID19_auto_register import main as CAR_main
from time import sleep


logger.info("Software started.")
if global_config.getRaw('config', 'enable') == 'true':
    while True:
        now_time = datetime.datetime.now()
        str_now_time = "{h}.{m}".format(h=now_time.hour, m=now_time.minute)
        str_set_time = global_config.getRaw('config', 'set_time')
        if  str_now_time == str_set_time:
            logger.info("Time arrived. Start to report.")
            CAR_main()
            sleep(65)
        else:
            sleep(1)
else:
    CAR_main()
