# CDU-ISP-AutoReport

[![License](https://img.shields.io/github/license/BenjiaH/CDU-ISP-AutoReport.svg)](https://github.com/BenjiaH/CDU-ISP-AutoReport/blob/master/LICENSE)
[![Release](https://img.shields.io/github/release/BenjiaH/CDU-ISP-AutoReport.svg)](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/latest)
[![Release Date](https://img.shields.io/github/release-date/BenjiaH/CDU-ISP-AutoReport.svg)](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/latest)


[![Branch-main](https://img.shields.io/badge/branch-main-green)](https://github.com/BenjiaH/CDU-ISP-AutoReport/tree/main)
[![Branch-teacher](https://img.shields.io/badge/branch-teacher-green)](https://github.com/BenjiaH/CDU-ISP-AutoReport/tree/teacher)

```N/A
   _____ _____  _    _      _____  _____ _____                    _        _____                       _   
  / ____|  __ \| |  | |    |_   _|/ ____|  __ \        /\        | |      |  __ \                     | |  
 | |    | |  | | |  | |______| | | (___ | |__) ______ /  \  _   _| |_ ___ | |__) |___ _ __   ___  _ __| |_ 
 | |    | |  | | |  | |______| |  \___ \|  ___|______/ /\ \| | | | __/ _ \|  _  // _ | '_ \ / _ \| '__| __|
 | |____| |__| | |__| |     _| |_ ____) | |         / ____ | |_| | || (_) | | \ |  __| |_) | (_) | |  | |_ 
  \_____|_____/ \____/     |_____|_____/|_|        /_/    \_\__,_|\__\___/|_|  \_\___| .__/ \___/|_|   \__|
                                                                                     | |                   
                                                                                     |_|                   
```

A tool which helps you to report your physical condition on CDU-ISP during COVID-19 automatically.

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

## 1.托管

- 如果您为小白或新手且需要在我的服务器上为您进行自动化打卡服务，请填写[信息采集表](https://benjiah.gitee.io/redirect/cdu-isp-wjx)，我将每日为您定时打卡。

## 2.Features/TODO

- [X] 自动打卡
- [X] WeChat、邮件双通道推送结果
- [X] 定时执行
- [X] 多账户
- [X] 实时刷新配置文件
- [X] 高安全性：随机主机、随机`User-Agent`、HTTPS加密、SSL加密

## 3.安装依赖

```bash
pip install -r requirements.txt
```

## 4.使用方法

### 4.1.生成`sendkey`(用作微信推送)(可选)

- 打开[Server酱](https://benjiah.gitee.io/redirect/serversauce)。
- 申请一个`sendkey`，并记录下来。

### 4.2.填写[`config/config.json`](config/config_example.json)

- 重命名`config_example.json`文件为`config.json`。
- 参照[`config.json`文件](config/config_example.json)内说明填写其余内容。

### 4.3.填写[`config/account.csv`](config/account_example.csv)(可选)

- 重命名`account_example.csv`文件为`account.csv`。
- 仿照示例填写内容。
- 可录入多行信息，即可为多账户打卡。
- `wechat_push`值为`1`则代表当前账户选择微信推送，`email_push`同理。
- **注意：如果使用MS Excel打开CSV文件时，`studentID`极有可能被MS Excel自动更改格式，导致软件运行错误。推荐使用文本编辑软件进行填写。**

### 4.4.运行脚本

```bash
python main.py
```

- 在`Windows`平台下，你可以运行[`run.bat`](run.bat)

```bash
.\CDU-ISP-AutoReport\run.bat 
```

- 在`GNU/Linux`平台下，你可以运行[`run.sh`](run.sh)

```bash
chmod +x CDU-ISP-AutoReport/run.sh
./CDU-ISP-AutoReport/run.sh
```

## 5.CHANGE LOG

- [CHANGELOG.md](CHANGELOG.md)

## 6.程序结构

```N/A
│  .gitignore
│  CHANGELOG.md         <---更新日志
│  LICENSE
│  main.py              <---入口程序
│  README.md
│  run.bat              <---Windows下运行文件
│  run.sh               <---GNU/Linux下运行文件
│
├─common
│      account.py       <---多账户读取模块
│      config.py        <---配置读取模块
│      logger.py        <---日志模块
│      push.py          <---推送模块
│      report.py        <---自动化报告模块
│      service.py       <---服务管理模块
│      utils.py         <---工具模块
│
├─config
│      account.csv      <---多账户管理文件
│      config.json      <---配置文件
│      email_tmpl.html  <---Email模板文件
│
└─log
       log.log          <---日志文件

```

## 7.致谢

- [easychen/wecomchan](https://github.com/easychen/wecomchan/blob/main/LICENSE)
- [riba2534/wecomchan](https://github.com/riba2534/wecomchan/blob/main/LICENSE)
- [fake_useragent](https://github.com/hellysmile/fake-useragent/blob/master/LICENSE)
- [lxml](https://github.com/lxml/lxml/blob/master/LICENSES.txt)
- [requests](https://github.com/psf/requests/blob/main/LICENSE)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
- [loguru](https://github.com/Delgan/loguru/blob/master/LICENSE)
- [retrying](https://github.com/rholder/retrying/blob/master/LICENSE)
