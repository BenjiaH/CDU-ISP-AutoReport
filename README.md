# CDU-ISP-AutoReport

A tool which helps you to report your physical condition on CDU-ISP during COVID19 automatically.

## 特别声明

- 本仓库发布的`CDU-ISP-AutoReport`项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

- 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。

- 本仓库拥有者对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.

- 间接使用脚本的任何用户，包括但不限于建立VPS或在某些行为违反国家/地区法律或相关法规的情况下进行传播, 本仓库拥有者对于由此引起的任何隐私泄漏或其他后果概不负责。

- 请勿将`CDU-ISP-AutoReport`项目的任何内容用于商业或非法目的，否则后果自负。

- 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关脚本。

- 以任何方式查看此项目的人或直接或间接使用`CDU-ISP-AutoReport`项目的任何脚本的使用者都应仔细阅读此声明。本仓库拥有者保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或`CDU-ISP-AutoReport`项目，则视为您已接受此免责声明。
  
- 您必须在下载后的24小时内从计算机或手机中完全删除以上内容。

- 本项目遵循[`GPL-3.0 License`](LICENSE)协议，如果本特别声明与`GPL-3.0 License`协议有冲突之处，以本特别声明为准。

## 1.Features

- 自动打卡
- Wechat、邮件推送结果
- 定时执行
- 多账户
- 实时刷新配置文件
- 高安全性：随机主机、随机`User-Agent`

## 2.TODO

- [X] Wechat推送更多内容
- [X] 定时执行
- [X] 多账户
- [X] 邮件推送
- [X] 增加安全性：随机主机、随机`User-Agent`

## 3.安装第三方库

`pip install -r requirements.txt`

## 4.使用方法

### 4.1.生成`sckey`(推荐)

- 打开[Server酱](https://benjiah.gitee.io/redirect/serversauce)。
- 申请一个`sckey`，并记录下来。

### 4.2.填写[`config.ini`](config_template.ini)

- 重命名`config_template.ini`文件为`config.ini`。
- 填写`studentID`为学号。
- 填写`password`为CDU-ISP登录密码(**为保证账号安全，建议提前修改登录密码！！！**)。
- 填写`sckey`。

### 4.3.填写[`account.csv`](account_template.csv)(可选)

- 重命名`account_template.csv`文件为`account.csv`。
- 仿照示例填写内容。
- `wechat_push`值为`1`则代表当前账户选择微信推送，`email_push`同理。
- **注意：如果使用MS Excel打开CSV文件时，`studentID`极有可能被MS Excel自动更改格式，导致软件运行错误。推荐使用文本编辑软件进行填写。**

### 4.4.运行脚本

`python main.py`

- 在`Windows`平台下，你可以直接运行[`run.bat`](run.bat)
- 在`Linux`平台下，你可以直接运行[`run.sh`](run.sh)

## 5.托管

- 如果需要在我的服务器上为你的打卡服务进行托管，请填写[信息采集表](https://benjiah.gitee.io/redirect/cdu-isp-wjx)。
