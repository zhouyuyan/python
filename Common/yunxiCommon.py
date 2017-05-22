#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/3 14:14
import os
import traceback
import logging
import datetime
import pexpect, sys, os.path, subprocess


def desired_caps(self):
    caps = {

        'platformName': 'Android',

        'platformVersion': '6.0',

        'deviceName': 'Q4YTZ9PRS4CQFMCE',

        'appPackage': 'tv.yunxi.app',

        'appActivity': 'tv.yunxi.app.module.common.MainActivity',

        # 'app': "D:\DevelopTools\Android\sdk\platform-tools",

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
