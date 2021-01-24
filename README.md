# COVID19_auto_register

A tool which helps you to report your physical condition during COVID19 automatically.

## 安装第三方库

`pip install -r requirements.txt`

## 使用方法

### 使用Chrome浏览器(推荐)

### [登录 CDU-ISP](https://xsswzx.cdu.edu.cn/ispstu1-2/com_user/webindex.asp)

### 打开疫情信息登记栏并获取`id`和`cookie`

- 打开开发人员工具(<kbd>F12</kbd>),选择网络选项卡(Network)，并勾选保存日志(Preserve log)。
- 打开疫情信息登记页面，在开发人员工具种找到`project.asp?id=XXXXXXXXXXX`这条日志。记录此处`id=XXXXXX`(只需记录等于后面的内容)。
- 单击此条日志。在标头(Headers)中找到`Cookie`。记录此处`Cookie: XXXX`(只需记录等于后面的内容)。

### 生成`sckey`

- [打开Server酱](http://sc.ftqq.com/3.version)
- 申请一个`sckey`，并记录下来。

### 修改`config.ini`文件

- 重命名`config_template.ini`文件为`config.ini`
- 分别填写刚才记录的`cookie`, `id`和`sckey`(无需引号)。

### 运行脚本

`python COVID19_auto_register.py`

或

运行`run.bat`
