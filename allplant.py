import requests
import json
import sqlite3
import time
from os import path
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from urllib import request
from http import cookiejar

# 使用cursor()方法获取操作游标

d = path.dirname(__file__)
db = sqlite3.connect(path.abspath(d)+'\\/all.db')

#定义获取cookie字典值方法
def getcookie(url):
    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler=request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    response = opener.open(url)
    # 打印cookie信息
    a=[]
    for item in cookie:
        a.append(str(item.name+'='+item.value))
    return(a)


#定义方法插入数据库记录
def insupdb(queryResults,artt,artc,cret,mait,modf,pltpy):
    cursor = db.cursor()
    for i in range(len(queryResults)):
        sqlselect = 'SELECT count(1) FROM Channel where indexid=%s and planttype=\'%s\'' % (
            queryResults[i]['id'],pltpy)
        cursor.execute(sqlselect)
        db.commit()
        selectid = cursor.fetchall()

        if selectid[0][0] == 0:  # 判断当前公告ID是否已经插入数据表
            ids = queryResults[i]['id']
            articleTitle = queryResults[i][artt]
            articleChannelId = queryResults[i][artc]
            created = queryResults[i][cret]
            mailtext = queryResults[i][mait]
            modified = queryResults[i][modf]
            # SQL 插入语句
            sql = 'INSERT INTO Channel(indexid,articleTitle, articleChannelId, created, modified,status,mailtext,planttype)VALUES (%s,\'%s\',%s,\'%s\',\'%s\',0,\'%s\',\'%s\')' % (
                ids, articleTitle, articleChannelId, created, modified, mailtext,pltpy)
            cursor.execute(sql)
            db.commit()
        else:
            pass


#邮件相关参数准备
my_sender = 'xxxx@xxxx.com'    # 发件人邮箱账号
my_pass = 'xxxx'              # 发件人邮箱密码(当时申请smtp给的口令)
my_user = 'xxxx@xxxx.com'      # 收件人邮箱账号，我这边发送给自己

#定义发送邮件方法
def mail(planttype,articleTitle, mailtext):
    ret = True
    try:
        msg = MIMEText(mailtext, 'html', 'utf-8')
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr([planttype+"开放平台", my_sender])
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = formataddr(["公告推送机器人", my_user])
        # 邮件的主题，也可以说是标题
        msg['Subject'] = articleTitle

        # 发件人邮箱中的SMTP服务器，端口是465
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

#定义执行发送邮件方法
def setmail(mailid,planttype,articleTitle, mailtext):
    ret = mail(planttype,articleTitle, mailtext)
    if ret:
        sqlupdatestatus = 'UPDATE Channel set `status`=1 where indexid=%s' % (
            mailid)
        cursor.execute(sqlupdatestatus)
        db.commit()
        print("主题：【%s】%s 邮件发送成功" % (mailid, articleTitle))
    else:
        print("主题：【%s】%s 邮件发送失败" % (mailid, articleTitle))
    time.sleep(100)




#获取淘宝开放平台主页cookie
cookietext = getcookie('https://open.taobao.com/announcement.htm?docId=0&docType=11')

#获取主页公告列表
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36', 'Cookie': 'thw=cn; cna=WHXhFd+OEiMCAbRrQnvjfnrl; tracknick=%5Cu8000%5Cu967D%5Cu901B%5Cu901B; tg=0; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; miid=450144971720217721; UM_distinctid=16f9007feb042b-008f32d96467d2-7373e61-1fa400-16f9007feb26ce; '+cookietext[2]+'; enc=761dngOM%2BHCoraQ2tNp0bfVO8qRasL%2FpjmRFtf95nz%2FEAAObKSZjxwustVXQCv2hgiP0tLwKvcDeI2G0eTqjnQ%3D%3D; sgcookie=EitJWnkqbDTVPULpaxm9o; uc3=vt3=F8dBxd9lqfUQTp3bQ58%3D&nk2=sbDBiijQ9Q8%3D&id2=UoTZ4SWFLIWn&lg2=VFC%2FuZ9ayeYq2g%3D%3D; lgc=%5Cu8000%5Cu967D%5Cu901B%5Cu901B; uc4=nk4=0%40s9WXTHCxcYCNhX9Y3AgOADBovw%3D%3D&id4=0%40UOxzIE9vC3bdEorFn4nUhUsGhHY%3D; _cc_=Vq8l%2BKCLiw%3D%3D; _m_h5_tk=7291f9f71e382ce23bf9eb22dc3e8fd7_1586448931070; _m_h5_tk_enc=0a094935921b08670ffc25cd1201792c; tfstk=cAIGBi4s0N8_w7FCIft1HwifalrRZAm2ZiSCYGSR3q8vaEjFi23EkvQLKCfGDq1..; v=0; '+cookietext[1]+'; '+cookietext[0]+'; isg=BPT0Iq9YFrNWBYEEgx6xPRvYxbJmzRi3kAZ7lo5Xi38C-ZVDtttYRo34fTEhAVAP; l=eBP3GWWuqKgp1db-BO5wSbdaM7QTnQAb8sPy2o_niIHca6IROFZ8xNQceCE65dtjgt5jgetPrSLOTRFHkSa38AkDBeYIDMPcrM9p8e1..'}
urljd='https://open.jd.com/doc/getNewJosChannelInfo?channelId=&pageIndex='
urltb = 'https://open.taobao.com/handler/document/getDocument.json?isEn=false&treeId=&docId=0&docType=11&%s' %(cookietext[0])

#按平台区分，分别下载公告ID和抬头
planttype=['tb','jd']
for pi in planttype:
    if pi=='tb':
        #主页获取部分
        html = requests.get(urltb, headers=headers)
        jsob = json.loads(html.text)
        responseData = jsob.get('data')
        queryResults = responseData.get('queryResults')
        #主页数据插入
        articleTitle='title'
        articleChannelId='docType'
        created='gmtModified'
        mailtext='url'
        modified='gmtModified'
        insupdb(queryResults,articleTitle,articleChannelId,created,mailtext,modified,pi)
    elif pi=='jd':
        #主页获取部分
        html = requests.get(urljd)
        jsob = json.loads(html.text)
        responseData = jsob.get('responseData')
        queryResults = responseData['josCmsArticle']
        #主页数据插入
        articleTitle='articleTitle'
        articleChannelId='articleChannelId'
        created='created'
        mailtext='articleChannelId'
        modified='modified'
        insupdb(queryResults,articleTitle,articleChannelId,created,mailtext,modified,pi)


#邮件发送
#查询所有未发送状态的公告行
sqlmail = 'SELECT indexid,articleTitle,mailtext,planttype FROM Channel where status=0'
cursor = db.cursor()
cursor.execute(sqlmail)
db.commit()
mailindex = cursor.fetchall()

for i in range(len(mailindex)):
    indexid=mailindex[i-1][0]
    articleTitle=mailindex[i-1][1]
    mailtext = mailindex[i-1][2]
    planttype=mailindex[i-1][3]
    if planttype =='tb':
        #查询淘宝公告详情页
        planttypename='淘宝'
        cookietextitem = getcookie('https://open.taobao.com%s' % (mailtext))
        headersitem = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36', 'Cookie': 'thw=cn; cna=WHXhFd+OEiMCAbRrQnvjfnrl; tracknick=%5Cu8000%5Cu967D%5Cu901B%5Cu901B; tg=0; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; miid=450144971720217721; UM_distinctid=16f9007feb042b-008f32d96467d2-7373e61-1fa400-16f9007feb26ce; '+cookietextitem[2]+'; enc=761dngOM%2BHCoraQ2tNp0bfVO8qRasL%2FpjmRFtf95nz%2FEAAObKSZjxwustVXQCv2hgiP0tLwKvcDeI2G0eTqjnQ%3D%3D; sgcookie=EitJWnkqbDTVPULpaxm9o; uc3=vt3=F8dBxd9lqfUQTp3bQ58%3D&nk2=sbDBiijQ9Q8%3D&id2=UoTZ4SWFLIWn&lg2=VFC%2FuZ9ayeYq2g%3D%3D; lgc=%5Cu8000%5Cu967D%5Cu901B%5Cu901B; uc4=nk4=0%40s9WXTHCxcYCNhX9Y3AgOADBovw%3D%3D&id4=0%40UOxzIE9vC3bdEorFn4nUhUsGhHY%3D; _cc_=Vq8l%2BKCLiw%3D%3D; _m_h5_tk=7291f9f71e382ce23bf9eb22dc3e8fd7_1586448931070; _m_h5_tk_enc=0a094935921b08670ffc25cd1201792c; tfstk=cAIGBi4s0N8_w7FCIft1HwifalrRZAm2ZiSCYGSR3q8vaEjFi23EkvQLKCfGDq1..; v=0; '+cookietextitem[1]+'; '+cookietextitem[0]+'; isg=BMDAv7KOiheGQnXoVxq9GbeUkU6SSaQTjNovejpRyFtutWHf4louosLEyR11BVzr; l=eBP3GWWuqKgp1DHKBOfNdbdaM7Q9KIRfgu-RbwbkiT5POvfB5JUGWZXJ2K86CnGVnsg2R37uMFCUB0Tiuy4e7xv9-eiAYSbuFdTh.'}
        urlitem = 'https://open.taobao.com/handler/document/getDocument.json?isEn=false&treeId=&docId=%s&docType=12&%s' % (indexid,cookietextitem[0])
        jsobitem = json.loads(requests.get(urlitem, headers=headersitem).text)
        responseData = jsobitem.get('data')
        mailinfo = responseData.get('content')
    elif planttype =='jd':
        planttypename='京东'
        #查询京东公告详情页
        urlitem = 'https://open.jd.com/doc/getArticleDetailInfo?articleId=%s' % (indexid)
        jsobitem = json.loads(requests.get(urlitem, headers=headers).text)
        mailinfo = jsobitem['responseData']['articleContent']
    #执行邮件发送
    setmail(indexid,planttypename,articleTitle,mailinfo)

# 关闭数据库连接
db.close()

