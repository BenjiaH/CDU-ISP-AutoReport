import datetime

from common.account import global_account
from common.push import global_push
from common.logger import logger
from time import sleep

title = "Title"
message = "Message"

global_account.refresh()
global_push.bot_email.login()
n = global_account.row
for i in range(n):
    message = str(datetime.datetime.now()) + "\n" + message
    logger.info("{i}/{n} Sending... ID:{studentID}.".format(i=i + 1, n=n, studentID=global_account.studentID[i]))
    global_push.bot_email.send(title, message, [global_account.email[i]])
    global_push.wechat(title, message, global_account.sckey[i])
    sleep(2)
