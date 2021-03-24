# 请确保已打开全局开关(multiple_enable,wechat_enable,email_enable)
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
    uid = global_account.studentID[i]
    logger.info("{i}/{n} Sending... ID:{studentID}.".format(i=i + 1, n=n, studentID=global_account.studentID[i]))
    global_push.bot_email.send(uid, title, message, [global_account.email[i]])
    global_push.wechat(uid, title, message, global_account.sckey[i])
    sleep(1.5)
