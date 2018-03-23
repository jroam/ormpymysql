#coding=utf-8
'''
这里是常用函数库
'''
import os
import re
import smtplib
from email.mime.text import MIMEText
import urllib.request
import email
from email.mime.multipart import MIMEMultipart
from email.header import Header
import random
import time
import sys


def echo(strs):
    print("tttt"+strs)

def getrestr(strs,patter,n=0):
    '''
    获取正则匹配的第一项,如果没有找到返回空字符串
    strs 是源字符串
    patter 正则表达式
    n 当为0时，表示返回整个找到的内容的第一项，当大于0时，表示返回第几个括号里找到的内容
    '''
    result=""
    m = re.search(patter, strs)
    if m:
       if n==0:
           result=m.group(0)
       else:
           result=m.group(n)
    else:
        result=""
    return result


def sendmail(title,content,tomail):
    '''发送电子邮件'''
    ziphanghao=[["kd1a1e02mzl001@163.com","smtp.163.com","kd1a1e024d7g1"],
                ["dreamstravel@qq.com","smtp.qq.com","2dhj000"],
                ["kd8a4emzl@163.com","smtp.163.com","kd8a4e224d7b1"]
    ]


    zhao=random.choice(ziphanghao) #随机获取一个发件帐号
    MAIL_FROM=zhao[0]
    MAIL_TO = [tomail,"net1@dreams-travel.com"]
    msg = MIMEText(content,"html",_charset='utf-8')
    msg['Subject'] = Header(title,'utf-8')
    msg['From'] = MAIL_FROM
    try:
        smtp = smtplib.SMTP()
        smtp.connect(zhao[1])
        print(zhao[0])
        smtp.login(re.sub(r'\@[\w\-\.]+','',zhao[0]), zhao[2])#用户名和密码
        smtp.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())
        return True
    except Exception as e:
        return e

def isset(str1):
    '''判断一个应对量是否已经定义'''
    try:
        type(str1)
    except :
        return True
    else:
        return False



def file_get_content(url):
    '''远程抓取页面内容或打开本地文件'''
    if re.search("^http://",url):
        try:
            cc=urllib.request.urlopen(url).read()
            cc=cc.decode("utf-8")
            return cc
        except:
            return ""
    else:
        try:
            f=open(url,"r")
            a=f.read()
            f.close()
        except:
            a=""
        return a


def mkdir(path):
    '''执行创建多重文件夹目录'''
    path=path.strip()
    path=path.rstrip("\\")

    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def file_put_content(filename,strs,mod="a"):
    '''写入文件，若没有会自动创建,
        成功返回true 失败返回False
    '''
    try:
        
        f=open(filename,mod,encoding='utf8')
        f.write(strs)
        f.close()
        return True
    except Exception as e:
        print(e)
        return False


def addlog(strs,filename=""):
    '''自动记录日志，以每天为一个文件
    filename 填写入口文件处为根目录的相对路径
    '''

    #timeArray = time.localtime(int(time.time()))
    oTime = time.strftime("%Y%m%d")
    
    if filename=="" : filename="/logs"
    mkdir(sys.path[0]+filename)
    filename=sys.path[0]+filename+"/"+str(oTime)+".txt"
    file_put_content(filename,strs+"\n","a+")


