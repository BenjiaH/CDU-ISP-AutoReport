# COVID19_auto_register

A tool which helps you to report your physical condition during COVID19 automatically.

## 安装第三方库

`pip install -r requirements.txt`

## 使用方法

### 生成`sckey`(推荐)

- 打开[Server酱](https://benjiah.gitee.io/redirect/serversauce)。
- 申请一个`sckey`，并记录下来。

### 填写`config.ini`

- 重命名`config_template.ini`文件为`config.ini`。
- 填写`studentID`为学号(无需引号)。
- 填写`password`为CDU-ISP登录密码(无需引号。**为保证账号安全，建议提前修改登录密码！！！**)。
- 填写`sckey`。

### 运行脚本

`python main.py`

或

运行`run.bat`

## TODO

- [X] Wechat推送更多内容
- [X] 定时执行
- [ ] 支持多账户
