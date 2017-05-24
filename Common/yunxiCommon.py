#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/3 14:14
import os
import traceback
import logging
import datetime
import pexpect, sys, os.path, subprocess


def desired_caps():
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


def get_id(self, id):
    element = self.driver.find_element_by_id(id)
    return element


def get_name(self, name):
    element = self.driver.find_element_by_name(name)
    return element


def over(self):
    element = self.driver.quit()
    return element


def get_screen(self, path):
    self.driver.get_screenshot_as_file(path)


def get_size(self):
    size = self.driver.get_window_size()
    return size


def swipe_to_up(self):
    window_size = self.get_size()
    width = window_size.get("width")
    height = window_size.get("height")
    self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4, 500)


def swipe_to_down(self):
    window_size = self.get_size()
    width = window_size.get("width")
    height = window_size.get("height")
    self.driver.swipe(width / 2, height / 4, width / 2, height * 3 / 4, 500)


def swipe_to_left(self):
    window_size = self.get_size()
    width = window_size.get("width")
    height = window_size.get("height")
    self.driver.swipe(width / 4, height / 2, width * 3 / 4, height / 2, 500)


def swipe_to_right(self):
    window_size = self.get_size()
    width = window_size.get("width")
    height = window_size.get("height")
    self.driver.swipe(width * 4 / 5, height / 2, width / 5, height / 2, 500)


def back(self):
    self.driver.keyevent(4)


def get_classes(self, classesname):
    elements = self.driver.find_elements_by_class_name(classesname)
    return elements


def get_ids(self, ids):
    elements = self.driver.find_elements_by_id(ids)
    return elements
