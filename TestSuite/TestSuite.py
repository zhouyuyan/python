__author__ = 'yongkang'
# coding=utf-8

import unittest
import os
import HTMLTestRunner
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


# 遍历测试用例
# 遍历测试用例
def creatsuite():
    testunit = unittest.TestSuite()
    test_dir = 'D:\\workspace\\yunxiAndroid\\TestCase'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py', top_level_dir=None)
    for testcase in discover:
        testunit.addTests(testcase)
    return testunit


# 生成测试报告
now = time.strftime('%Y-%m-%d_%H-%M-%S')
filename = 'D:\\Test_report\\' + now + '.html'
fp = open(filename, 'wb')
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'yunxizhibo_Android测试报告' + now, description=u'测试结果')


# 发送邮件
def sendmail(file_new):
    # 读取报告内容
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()

    mail_host = 'smtp.qq.com'
    mail_user = '791430360@qq.com'
    mail_pass = 'xhiuqsvtdokebcge'

    # 发送附件
    nowtime = time.strftime('%Y-%m-%d')
    msg = MIMEMultipart()
    part = MIMEText(open(file_new, 'rb').read(), 'base64', 'utf-8')
    part.add_header('Content-Disposition', 'attachment', filename="测试报告" + nowtime + ".html")
    msg.attach(part)

    # 设置收发件人信息和邮件主题
    msg.attach(MIMEText(mail_body, 'html', 'utf-8'))
    msg['From'] = '791430360@qq.com'
    msg['To'] = '2434665131@qq.com'
    msg['Subject'] = "APP_Android测试报告" + nowtime
    # smtp = smtplib.SMTP()
    smtp = smtplib.SMTP_SSL(mail_host)
    smtp.set_debuglevel(1)
    smtp.ehlo(mail_host)
    smtp.login(mail_user, mail_pass)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()


def sendreport():
    # 获取最新的报告
    report_dir = 'D:\\Test_report\\'
    lists = os.listdir(report_dir)
    lists.sort()
    file_new = os.path.join(report_dir, lists[-1])
    sendmail(file_new)


if __name__ == '__main__':
    runner.run(creatsuite())
    fp.close()
    time.sleep(3)
    sendreport()
