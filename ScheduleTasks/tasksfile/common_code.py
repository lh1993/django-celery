# -*- coding: utf-8 -*-
# @Time    : 2019/1/7 13:33
# @Author  : JY.Liu
# @Site    : http://github.com/lh1993
# @Mail    : lhln0119@163.com
# @File    : common_code.py
# @Software: PyCharm

from DataCenter.settings import redis_host, basegateway_url, corpid, corpsecret, email_username, email_password
from decimal import Decimal
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import smtplib
import pymysql as MySQLdb
import json
import requests
import redis
import time
import traceback


class Sql(object):

    def __init__(self, username, password, db, host, sql):
        self.username = username
        self.password = password
        self.db = db
        self.host = host
        self.sql = sql
        self.db_connect = MySQLdb.connect(
            db=self.db,
            host=self.host,
            user=self.username,
            passwd=self.password,
            charset="utf8")

    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, date):
            return str(obj)
        raise TypeError(
            "Object of type '%s' is not JSON serializable" %
            type(obj).__name__)

    def get_data(self, sql_data):
        """查询结果json序列化"""
        data_list = []
        for data in sql_data:
            data_list.append(list(data))
        return json.dumps(data_list, default=self.default)

    def get_row(self):
        """获取sql查询结果"""
        db_cursor = self.db_connect.cursor()
        db_cursor.execute(self.sql)
        row = db_cursor.fetchall()
        data = self.get_data(row)
        return data


class Redis(object):

    def __init__(self, host=redis_host, port="6379", db=0):
        self.redis_host = host
        self.redis_port = port
        self.r = redis.Redis(host=self.redis_host, port=self.redis_port, db=db)

    # 待修改
    def __setitem__(self, k, v):
        self.k = v

    def delete(self, value):
        return self.r.delete(value)

    def set(self, key, value):
        return self.r.set(key, value)

    def get(self, value):
        return self.r.get(value)


class WeChat(object):

    def __init__(self, touser=None, toparty=None, totag=None, agentid=None):
        self.url = basegateway_url
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.touser = touser
        self.toparty = toparty
        self.totag = totag
        self.agentid = agentid

    def get_access_token(self):
        # url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" %(self.corpid, self.corpsecret)
        # r = requests.get(url=url)
        # access_token = r.json()['access_token']
        access_token = self.rpc_resource_pull('qyweixin_access_token')
        return access_token

    '''
        获取XwjrRpc服务的公共资源接口
        如:企业微信access_token等
    '''
    def rpc_resource_pull(self, resource_key):
        if resource_key is None or resource_key is '':
            return ''
        req_data = {
            'pull_resource': resource_key
        }
        res_data = requests.post(self.url, data=req_data)
        data_value = res_data.json()[resource_key]
        return data_value

    def get_tag_list(self):
        access_token = self.get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/tag/list?access_token=%s" % access_token
        res = requests.get(url=url)
        return res.json()

    def get_agent_list(self):
        access_token = self.get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/agent/list?access_token=%s" % access_token
        res = requests.get(url=url)
        return res.json()

    def get_tag_users(self, tagid):
        access_token = self.get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/tag/get?access_token=%s&tagid=%s" % (
            access_token, tagid)
        res = requests.get(url=url)
        return res.json()

    def send_image(self, image_filename):
        files = {'files': open(image_filename, 'rb')}
        print(files)
        data = {
            "touser": self.touser,
            "toparty": self.toparty,
            "totag": self.totag,
            "agentid": self.agentid,
            "msgtype": "image",
            "safe": "0"}

        r = requests.post(url=self.url, data=data, files=files)
        res = r.json()
        print(res)
        if str(res['errcode']) == '0':
            return r.json()
        else:
            r = requests.post(url=self.url, data=data, files=files)
            res = r.json()
            print(res)
            if str(res['errcode']) != '0':
                print(res)
                raise SystemError(res)
            return r.json()


    def send_text(self, content):
        data = {
            "touser": self.touser,
            "toparty": self.toparty,
            "totag": self.totag,
            "agentid": self.agentid,
            "msgtype": "text",
            "content": content,
            "safe": "0"}

        r = requests.post(url=self.url, data=data)
        res = r.json()
        print(res)
        if str(res['errcode']) != '0':
            r = requests.post(url=self.url, data=data)
            res = r.json()
            print(res)
            if str(res['errcode']) != '0':
                raise SystemError(res)
        return r.json()

    def send_textcard(self, textcard):
        access_token = self.get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % access_token
        data = {
            "touser": self.touser,
            "toparty": self.toparty,
            "totag": self.totag,
            "agentid": self.agentid,
            "msgtype": "textcard",
            "textcard": textcard,
            "enable_id_trans": 0}

        r = requests.post(url=url, data=json.dumps(data))
        res = r.json()
        if str(res['errcode']) != '0':
            r = requests.post(url=url, data=json.dumps(data))
            res = r.json()
            if str(res['errcode']) != '0':
                raise SystemError(res)
        return r.json()

    def send_news(self, news):
        access_token = self.get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % access_token
        data = {
            "touser": self.touser,
            "toparty": self.toparty,
            "totag": self.totag,
            "agentid": self.agentid,
            "msgtype": "news",
            "news": news,
            "enable_id_trans": 0}

        r = requests.post(url=url, data=json.dumps(data))
        res = r.json()
        if str(res['errcode']) != '0':
            r = requests.post(url=url, data=json.dumps(data))
            res = r.json()
            if str(res['errcode']) != '0':
                raise SystemError(res)
        return r.json()


class Email(object):
    """Email发送"""

    def __init__(self, type):
        self.sender = email_username
        self.username = email_username
        self.password = email_password
        self.smtp = "smtp.mxhichina.com"
        self.type = type
        self.today = time.strftime('%Y%m%d', time.localtime(time.time()))

    def sys_alarm(self, subject, receivers, message):
        """任务异常，告警通知"""

        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = r"%s <%s>" % (
            Header(subject, 'utf-8'), self.sender)
        msgRoot['To'] = ';'.join(receivers)
        msgRoot['Subject'] = Header("%s-%s" %
                                    (subject, self.today), 'utf-8')
        mail_body = """
        <b>名称：</b> %s<br><br>
        <b>任务：</b> %s<br><br>
        <b>错误信息：</b><br>%s
        """ % tuple(message)
        msg = MIMEText(mail_body, 'html', 'utf-8')
        msgRoot.attach(msg)
        return msgRoot

    def html_notify(self, subject, receivers, message):
        """html格式邮件模板"""

        msgRoot = MIMEMultipart('alternatvie')
        msgRoot['Subject'] = Header("%s-%s" %
                                    (subject, self.today), 'utf-8')  # 组装信头
        msgRoot['From'] = r"%s <notify@xwjr.com>" % Header(subject, "utf-8")
        msgRoot['To'] = ';'.join(receivers)
        html_part = MIMEText(message, 'html', 'utf-8')
        msgRoot.attach(html_part)
        return msgRoot

    def attachment(self, subject, receivers, content, filepath, filename):
        """正文+附件邮件模板"""
        
        msgRoot = MIMEMultipart()
        msgRoot['Subject'] = Header("%s-%s" %
                                    (subject, self.today), 'utf-8')
        msgRoot['From'] = r"%s <notify@xwjr.com>" % Header(subject, "utf-8")
        msgRoot['To'] = ';'.join(receivers)
        # 添加邮件内容
        text_content = MIMEText(content)
        msgRoot.attach(text_content)
        # 添加附件
        file = filepath + filename
        print(file)
        with open(file, 'rb') as f:
            annex = MIMEApplication(f.read())
            annex.add_header(
                'Content-Disposition',
                'attachment',
                filename=filename)
        msgRoot.attach(annex)
        return msgRoot

    def send_mail(self, subject="数据推送中心", receivers=None, message=None, filepath=None, filename=None):
        """发送邮件"""
        receiver = []
        for item in receivers.split(";"):
            receiver.append(item)
        print(receiver)
        if self.type == "alarm":
            msgRoot = self.sys_alarm(
                subject=subject,
                receivers=receiver,
                message=message)
        elif self.type == "html_notify":
            msgRoot = self.html_notify(
                subject=subject,
                receivers=receiver,
                message=message)
        elif self.type == "attachment":
            msgRoot = self.attachment(
                subject=subject,
                receivers=receiver,
                content=message,
                filepath=filepath,
                filename=filename)
        else:
            return "发送异常，请添加type参数:alarm|html_notify"
        smtp = smtplib.SMTP('smtp.mxhichina.com')
        try:
            # 用户登陆邮箱，需要先将客户端授权开启，下面的密码是授权码
            smtp.login(self.username, self.password)
            print("准备发邮件")
            smtp.sendmail(
                self.sender,
                receiver,
                msgRoot.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")
            traceback.print_exc()
        finally:
            smtp.quit()
