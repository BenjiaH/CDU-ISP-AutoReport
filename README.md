# CDU-ISP-AutoReport

A tool which helps you to report your physical condition on CDU-ISP during COVID19 automatically.

## 1.Features

- 自动打卡
- Wechat推送结果
- 定时执行
- 多账户

## 2.TODO

- [X] Wechat推送更多内容
- [X] 定时执行
- [X] 多账户
- [ ] 邮件推送

## 3.安装第三方库

`pip install -r requirements.txt`

## 4.使用方法

### 4.1.生成`sckey`(推荐)

- 打开[Server酱](https://benjiah.gitee.io/redirect/serversauce)。
- 申请一个`sckey`，并记录下来。

### 4.2.填写`config.ini`

- 重命名`config_template.ini`文件为`config.ini`。
- 填写`studentID`为学号。
- 填写`password`为CDU-ISP登录密码(**为保证账号安全，建议提前修改登录密码！！！**)。
- 填写`sckey`。

### 4.3.填写`account.csv`(可选)

- 重命名`account_template.csv`文件为`account.csv`。
- 填写内容。
- 目前尚不支持邮件推送，`method`和`email`可随意填写。
- **注意：如果使用MS Excel打卡CSV文件时，`studentID`极有可能被MS Excel自动更改格式，导致软件运行错误。推荐使用文本编辑软件进行填写。**

### 4.4.运行脚本

`python main.py`

或

运行`run.bat`

## 5.托管

- 如果需要在我的服务器上为你的打卡服务进行托管，请填写[信息采集表](https://benjiah.gitee.io/redirect/cdu-isp-wjx)。
