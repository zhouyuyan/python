#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/3 14:14
import os
import traceback
import logging
import datetime
from time import sleep
from Common.Element import *

import pexpect, sys, os.path, subprocess
from appium import webdriver

from Common.action import ElementActions
from utils.environment import Environment

env = Environment().get_environment_info()


def desired_caps(self):
    caps = {

        'platformName': env.devices[0].platform_name,

        'platformVersion': env.devices[0].platform_version,

        'deviceName': env.devices[0].device_name,

        'appPackage': env.app_package,

        'appActivity': env.app_activity,

        'app': env.apk,
        'automationName': 'Appium',
        'unicodeKeyboard': True,
        'resetKeyboard': True,
        'autoLaunch': True,
        'autoAcceptAlerts': True
    }
    return caps


def writeLog(self):
    # 组合日志文件名（当前文件名+当前时间）.比如：case_login_success_20150817192533
    basename = os.path.splitext(os.path.basename(__file__))[0]
    logFile = 'D:\\Test_report\\' + basename + "-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
    logging.basicConfig(filename=logFile)
    s = traceback.format_exc()
    logging.error(s)
    self.driver.get_screenshot_as_file("./" + logFile + "-screenshot_error.png")


"""
封装Appium中关于元素对象的方法
"""

""""登录页面测试步骤"""


def goto_login(self):
    global action
    action = ElementActions(driver=self.driver)
    sleep(2)
    my = get_name(self, '我的')
    check_my = lambda action: action.is_element_displayed(my)
    if check_my:
        my.click()
    sleep(2)
    try:

        lgbs = get_name(self, '登录')
        check_lgbs = lambda action: action.is_element_displayed(lgbs)
        if check_lgbs:
            lgbs.click()
        sleep(2)
    except:
        print("进入登录页面失败")


def login(self, username, verificationcode):
    sleep(2)
    try:
        usernameEt = get_id(self, 'tv.yunxi.app:id/ed_phone_num')
        self.assertIsNotNone(usernameEt)
        usernameEt.send_keys(username)
        print(u'--已经输入手机号--')
        sleep(2)
        # get_id(self,'tv.yunxi.app:id/tv_get_verification_first').click()
        # print(u'--获取验证码--')
        # sleep(2)
        et_ver = get_id(self, 'tv.yunxi.app:id/ed_verification')
        self.assertIsNotNone(et_ver)
        et_ver.send_keys(verificationcode)
        print(u'--已输入验证码--')
        sleep(2)

        get_id(self, 'tv.yunxi.app:id/tv_phone_login').click()
        print(u'--点击登录--')
        sleep(2)
        phone = get_id(self, 'tv.yunxi.app:id/tv_phone')
        Login_successful = self.assertEqual(phone.text, username)  # 判断是否登录成功
        if Login_successful == None:
            return True

    except:
        print(u'--登录失败--')
        sleep(2)


def wx_login(self):
    wxBnt = get_id(self, 'tv.yunxi.app:id/ll_wechat_login')
    self.assertIsNotNone(wxBnt)
    wxBnt.click()
    get_name(self, '确认登录').click()
    sleep(4)


def user_agree(self):
    sleep(4)

    try:
        agree = get_id(self, 'tv.yunxi.app:id/tv_agree')
        self.assertIsNotNone(agree)
        agree.click()
        title = get_id(self, 'tv.yunxi.app:id/tv_title')
        self.assertIsNotNone(title)
        agree = self.assertEqual(title.text, u"用户协议")
        if agree == None:
            return True

    except:
        print('failed')
    self.driver.keyevent(4)
