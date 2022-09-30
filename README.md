# Clockin-releasedEdition
### NWAFU自动打卡
> 本程序在Python3.6.8环境下开发

> 运行脚本后自动完成今日打卡


## 参数

> ['uid','success_message','email-adress','cookie','account','password']

| 参数 | 说明 | 取值 |
| :-----| :---- | :---: |
| uid                | 打卡系统中的个人id ||
| success_message    | 是否向你的邮箱发送打卡成功信息 | '0' or '1' |
| email-adress       | 你的邮箱地址 ||
| cookie             | 格式为'eai-sess=*?' ||
| account            | 学号 ||
| password           | 密码 ||

## 准备

在accounts.py中按规定设置参数

如果需要使用邮件提醒功能请完成post.py中mailsend函数中的有关参数

否则需要将success_message项的值填为'0'

以下参数是必须的:

*  success_message

以下参数是可选的(1、2项中必须选择其中一项):

*  cookie &nbsp; 仅填写此项时打卡提醒是临时的，有效期约2个月
*  account & password &nbsp; 永久有效
*  email-adress &nbsp; 不完成mailsend函数则不需要填写此项

以下参数请留空:

*  uid

## 安装依赖

```
$ pip install -r requirements.txt
```

## 启动程序

```
$ python post.py
```

## 使用Github的Action功能自动运行程序

只需下载本代码，将其上传到你新建的私有仓库中

然后在Action面板中点击启用即可

注意！不要使用Fork不然你的修改将是公开的！
