#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/19 14:35
import unittest
from time import sleep
from Common import yunxiCommon as yc
from TestCase.test_login import Login as lg
from appium import webdriver as appdriver


class My(unittest.TestCase):
    def setUp(self):

        self.driver = appdriver.Remote('http://localhost:4723/wd/hub', yc.desired_caps(self))

        self.driver.implicitly_wait(5)

        print("----------------setup-------------")

    def tearDown(self):
        print("-------------teardown------------------")
        self.driver.close_app()
        self.driver.quit()

    def test_e(self):
        """测试登录-设置（清除缓存）"""
        lg.login(self, '13071825896', '3279')
        self.setting()

    def setting(self):

        try:
            self.driver.find_element_by_id('tv.yunxi.app:id/rl_setting').click()
            print(u'--点击设置按钮--')
            sleep(2)
            self.driver.find_element_by_id('tv.yunxi.app:id/rl_wipe_cache').click()
            print(u'--点击清空缓存按钮--')
            sleep(2)
            self.driver.find_element_by_id('tv.yunxi.app:id/dialog_ok').click()
            sleep(2)
            print(u'--点击清空缓存dialog--')
        except:
            print(u'--操作失败--')
        sleep(2)
        self.driver.find_element_by_id('tv.yunxi.app:id/ll_back').click()
        sleep(2)

        self.driver.keyevent(4)  # 硬件返回
        sleep(2)
