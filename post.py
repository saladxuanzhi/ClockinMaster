import re
import time
import requests
import json
import smtplib
from account import account
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

#default_payload = {"zgfxdq":"0","mjry":"0","csmjry":"0","uid":uid,"date":t,"tw":"2","sfcxtz":"0","sfyyjc":"0","jcjgqr":"0","jcjg":"","sfjcbh":"0","sfcxzysx":"0","qksm":"","remark":"","address":"\u9655\u897f\u7701\u54b8\u9633\u5e02\u6768\u9675\u533a\u5927\u5be8\u8857\u9053\u897f\u5317\u519c\u6797\u79d1\u6280\u5927\u5b66\u5317\u6821\u533a\u0039\u53f7\u516c\u5bd3","area":"\u9655\u897f\u7701\u0020\u54b8\u9633\u5e02\u0020\u6768\u9675\u533a","province":"\u9655\u897f\u7701","city":"\u54b8\u9633\u5e02","geo_api_info":"{\"type\":\"complete\",\"info\":\"SUCCESS\",\"status\":1,\"fEa\":\"jsonp_348864_\",\"position\":{\"Q\":34.2858,\"R\":108.06624,\"lng\":108.06624,\"lat\":34.2858},\"message\":\"Get ipLocation success.Get address success.\",\"location_type\":\"ip\",\"accuracy\":null,\"isConverted\":true,\"addressComponent\":{\"citycode\":\"0910\",\"adcode\":\"610403\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\",\"building\":\"\",\"buildingType\":\"\",\"street\":\"\u897f\u519c\u8def\",\"streetNumber\":\"22\u53f7\",\"country\":\"\u4e2d\u56fd\",\"province\":\"\u9655\u897f\u7701\",\"city\":\"\u54b8\u9633\u5e02\",\"district\":\"\u6768\u9675\u533a\",\"towncode\":\"610403003000\",\"township\":\"\u5927\u5be8\u8857\u9053\"},\"formattedAddress\":\"\u9655\u897f\u7701\u54b8\u9633\u5e02\u6768\u9675\u533a\u5927\u5be8\u8857\u9053\u897f\u5317\u519c\u6797\u79d1\u6280\u5927\u5b66\u5317\u6821\u533a9\u53f7\u516c\u5bd3\",\"roads\":[],\"crosses\":[],\"pois\":[]}","created":1650571457,"sfzx":"0","sfjcwhry":"0","sfcyglq":"0","gllx":"","glksrq":"","jcbhlx":"","jcbhrq":"","sftjwh":"0","sftjhb":"0","fxyy":"\u5047\u671f\u7ed3\u675f","bztcyy":"4","fjsj":"0","sfjchbry":"0","sfjcqz":"","jcqzrq":"","jcwhryfs":"","jchbryfs":"","xjzd":"","szgj":"","sfsfbh":"0","jhfjrq":"","jhfjjtgj":"","jhfjhbcc":"","jhfjsftjwh":"0","jhfjsftjhb":"0","szsqsfybl":0,"sfygtjzzfj":0,"gtjzzfjsj":"","sfsqhzjkk":0,"sqhzjkkys":"","szcs":"","created_uid":0,"id":25673534,"gwszdd":"","sfyqjzgc":"","jrsfqzys":"","jrsfqzfy":""}
payload = {}


def getinfo():
    global account
    global payload
    url = "https://app.nwafu.edu.cn/ncov/wap/default/index"
    headers = {
        "Content-Type": "text/html; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
        "sec-ch-ua-platform": "Windows",
        'Cookie': account[3]
    }
    response=requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    #老版本获取uid的代码，已废弃
    #account[0] = re.search(r"\"uid\":\"(.*?)\"", script).group()[7:12]
    try:
        script = BeautifulSoup(response.text, 'html.parser').findAll("script")[8].text
        oldInfo = re.search(r"oldInfo: {(.*?)},$", script, re.MULTILINE).group()
        newData = re.search(r"def = {(.*?)};$", script, re.MULTILINE).group()
        newPayload = eval(newData[6:len(newData)-1])
        payload = eval(oldInfo[9:len(oldInfo)-1])
        t = time.strftime("%Y%m%d", time.localtime())
        payload['date'] = t
        payload['created'] = newPayload['created']
        payload['id'] = newPayload['id']
    except:
        print('获取上次打卡信息异常')
        mailsend('获取上次打卡信息异常', account[2])


def getcookies():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://app.nwafu.edu.cn",
        "Referer": "https://app.nwafu.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.nwafu.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "sec-ch-ua-platform": "Windows"
        }
    url = "https://app.nwafu.edu.cn/uc/wap/login/check"
    
    retry = 3
    while retry > 0:
        try:
            if account[4] != '' :
                payload = {'username':account[4],'password':account[5]}
                response = requests.post(url, data=payload, headers=headers)
                if json.loads(response.text)['m'] == '账号或密码错误':
                    print('账号或密码错误')
                    mailsend('账号或密码错误', account[2])
                else:
                    cookie_t = requests.utils.dict_from_cookiejar(response.cookies)
                    result = 'eai-sess=' + cookie_t['eai-sess']
                    account[3] = result
                    print('Successfully get the cookie.')
            break

        except:
            retry -= 1
            print('Get cookie failed! Retry remaining ' + str(retry))
            if retry < 0:
                print('Failed to get cookie!')
                mailsend('获取cookie失败!', account[2])


def mailsend (string,receiver):
    if account[1] == '1':
        mail_host = 'smtp.qq.com'  #以qq邮箱为例
        mail_user = '你的qq号'
        mail_pass = 'smtp密码'
        sender = account[2]
        receivers = [receiver]
        message = MIMEText(string,'plain','utf-8')
        message['Subject'] = '健康打卡'
        message['From'] = sender
        message['To'] = receivers[0]

        try:
            smtpObj = smtplib.SMTP_SSL(mail_host)
            smtpObj.login(mail_user,mail_pass) 
            smtpObj.sendmail(sender,receivers,message.as_string()) 
            smtpObj.quit() 
            print('Send email successfully')
        except smtplib.SMTPException as e:
            print('Failed to send email',e)

def post(cookie,flag,uid,receiver):
    try:
        if cookie != '':
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://app.nwafu.edu.cn",
                "Referer": "https://app.nwafu.edu.cn/ncov/wap/default/index",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "sec-ch-ua-platform": "Windows",
                "Cookie": cookie
                }
            url = "https://app.nwafu.edu.cn/ncov/wap/default/save"
            
            response = requests.post(url, data=payload, headers=headers).text

            c = json.loads(response)
            if '成功' in response :
                print('打卡成功')
                if flag == '1':
                    mailsend(time.strftime("%m-%d", time.localtime()) + '打卡成功,' + c['m'], receiver)
            elif '已经' in response :
                print(c['m'])
            elif '失效' in response :
                print('Cookies已失效')
                mailsend('打卡失败, Cookies已失效', receiver)
            else:
                print('打卡失败,' + c['m'])
                mailsend('打卡失败,' + c['m'], receiver)
        else:
            print('Without cookie!')

    except:
        print ("Failed!")
        #mailsend('cookies过期或程序异常，打卡失败' , receiver)


if __name__ == "__main__":
    getcookies()
    getinfo()
    post(account[3],account[1],account[0],account[2])