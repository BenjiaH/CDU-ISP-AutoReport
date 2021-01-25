# COVID19_auto_register

A tool which helps you to report your physical condition during COVID19 automatically.

## 安装第三方库

`pip install -r requirements.txt`

## 使用方法

### 填写`studentID`和`password`

- 重命名`config_template.ini`文件为`config.ini`。
- 填写`studentID`为学号(无需引号)。
- 填写`password`为CDU-ISP登录密码(无需引号。**为保证账号安全，建议提前修改登录密码！！！**)。

### 运行脚本

`python COVID19_auto_register.py`

或

运行`run.bat`

## TODO

- [X] Wechat推送更多内容
- [ ] 定时执行
- [ ] 支持多账户
