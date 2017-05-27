#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/19 14:35
import unittest
from Common.yunxiCommon import *
from appium import webdriver as appdriver
from Common.Element import *

from utils import L

L.i('-------开始运行test_login-------')


class Login(unittest.TestCase):
    def setUp(self):
        self.driver = appdriver.Remote('http://localhost:4723/wd/hub', desired_caps(self))

        self.driver.implicitly_wait(5)
        writeLog(self)
        global action
        action = ElementActions(driver=self.driver)
        # 判断是否出现权限弹窗
        time.sleep(3)
        # try:
        #
        #     els = self.driver.find_elements_by_class_name('android.widget.Button')
        #     for el in els:
        #         time.sleep(2)
        #         if el.text == u'允许':
        #             self.driver.find_element_by_android_uiautomator('new UiSelector().text("允许")').click()
        #             print('点击允许')
        #         elif el.text == u'始终允许':
        #             self.driver.find_element_by_android_uiautomator('new UiSelector().text("始终允许")').click()
        #             print('点击始终允许')
        #         elif el.text == u'确定':
        #             self.driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
        #             print('点击确定')
        # except:
        #     print('pass')
        #
        #     pass
        print("----------------setup-------------")

    def tearDown(self):
        print("-------------teardown------------------")
        self.driver.close_app()
        self.driver.quit()

    def test_login01(self):
        u"""用户名为空，密码为空----登录失败"""
        goto_login(self)

        a = login(self, '', '')
        self.assertFalse(a, False)

    def test_login02(self):
        u"""13071825896，密码为空----登录失败"""
        goto_login(self)

        a = login(self, '13071825896', '')
        self.assertFalse(a, False)

    def test_login03(self):
        u"""用户名为空，密码为3279----登录失败"""
        goto_login(self)

        a = login(self, '', '3279')
        self.assertFalse(a, False)

    def test_login04(self):
        u"""用户名为13071825896，密码为3279----登录成功"""
        goto_login(self)
        a = login(self, '13071825896', '3279')

        self.assertTrue(a, True)
        print('登录成功')

    def test_wxlogin(self):
        u"""微信登录"""

        goto_login(self)
        # self.wx_login()

    def test_userAgree(self):
        u"""用户协议----跳转成功"""
        goto_login(self)
        a = user_agree(self)
        print(a)
        self.assertTrue(a, True)


if __name__ == '__Login__':
    unittest.main()
