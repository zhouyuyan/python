#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/19 14:35
import unittest
from time import sleep
from Common import yunxiCommon as yc
from appium import webdriver as appdriver


class Login(unittest.TestCase):
    def setUp(self):

        self.driver = appdriver.Remote('http://localhost:4723/wd/hub', yc.desired_caps(self))

        self.driver.implicitly_wait(5)

        print("----------------setup-------------")

    def tearDown(self):
        print("-------------teardown------------------")
        self.driver.close_app()
        self.driver.quit()

    def test_login01(self):
        u"""用户名为空，密码为空----登录失败"""
        self.goto_login()

        a = self.login('', '')
        self.assertFalse(a, False)

    def test_login02(self):
        u"""13071825896，密码为空----登录失败"""
        self.goto_login()

        a = self.login('13071825896', '')
        self.assertFalse(a, False)

    def test_login03(self):
        u"""用户名为空，密码为3279----登录失败"""
        self.goto_login()

        a = self.login('', '3279')
        self.assertFalse(a, False)

    def test_login04(self):
        u"""用户名为13071825896，密码为3279----登录成功"""
        self.goto_login()

        a = self.login('13071825896', '3279')
        print(a)
        self.assertTrue(a, True)

    def test_wxlogin(self):
        u"""微信登录"""

        self.goto_login()
        self.wx_login()

    def test_userAgree(self):
        u"""用户协议----跳转成功"""
        self.goto_login()
        a = self.user_agree()
        print(a)
        self.assertTrue(a, True)

    def goto_login(self):
        try:
            my = self.driver.find_element_by_name('我的')
            self.assertIsNotNone(my)
            my.click()
            sleep(2)
            lgbs = self.driver.find_element_by_name('登录')
            self.assertIsNotNone(lgbs)
            lgbs.click()
            sleep(2)
        except:
            print("进入登录页面失败")

    def login(self, username, verificationcode):

        try:

            self.driver.find_element_by_id('tv.yunxi.app:id/ed_phone_num').send_keys(username)
            print(u'--已经输入手机号--')
            sleep(2)
            # self.driver.find_element_by_id('tv.yunxi.app:id/tv_get_verification_first').click()
            # print(u'--获取验证码--')
            # sleep(2)
            et_ver = self.driver.find_element_by_id('tv.yunxi.app:id/ed_verification')
            self.assertIsNotNone(et_ver)
            et_ver.send_keys(verificationcode)
            print(u'--已输入验证码--')
            sleep(2)
            self.driver.find_element_by_id('tv.yunxi.app:id/tv_phone_login').click()
            print(u'--点击登录--')
            sleep(2)
            phone = self.driver.find_element_by_id('tv.yunxi.app:id/tv_phone')
            Login_successful = self.assertEqual(phone.text, username)  # 判断是否登录成功
            if Login_successful == None:
                return True

        except:
            print(u'--密码超限，请稍后重试--')
            sleep(2)
        sleep(2)

    def wx_login(self):
        wxBnt = self.driver.find_element_by_id('tv.yunxi.app:id/ll_wechat_login')
        self.assertIsNotNone(wxBnt)
        wxBnt.click()
        self.driver.find_element_by_name(u'确认登录').click()
        sleep(4)

    def user_agree(self):
        sleep(4)

        try:
            agree = self.driver.find_element_by_id('tv.yunxi.app:id/tv_agree')
            self.assertIsNotNone(agree)
            agree.click()
            title = self.driver.find_element_by_id('tv.yunxi.app:id/tv_title')
            self.assertIsNotNone(title)
            agree = self.assertEqual(title.text, u"用户协议")
            if agree == None:
                return True

        except:
            print('failed')
        self.driver.keyevent(4)


if __name__ == '__main__':
    unittest.main()
