__author__ = 'yongkang'
# coding=utf-8

import unittest
import os
import HTMLTestRunner
import time
from Common.sendmail import *

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
