#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/19 14:35
import unittest

from Common.action import ElementActions
from Common.yunxiCommon import *
from Common.Element import *
from appium import webdriver as appdriver
from utils import L

L.i('-------开始运行test_my-------')


class My(unittest.TestCase):
    def setUp(self):

        self.driver = appdriver.Remote('http://localhost:4723/wd/hub', desired_caps(self))

        self.driver.implicitly_wait(5)
        writeLog(self)
        global action
        action = ElementActions(driver=self.driver)

        print("----------------setup-------------")

    def tearDown(self):
        print("-------------teardown------------------")
        self.driver.close_app()
        self.driver.quit()

    def test_e(self):
        """测试登录-设置（清除缓存）"""
        goto_login(self)
        login(self, '13071825896', '3279')
        self.setting()

    def setting(self):

        try:
            get_id(self, 'tv.yunxi.app:id/rl_setting').click()
            L.i('--点击设置按钮--')
            sleep(2)
            get_id(self, 'tv.yunxi.app:id/rl_wipe_cache').click()
            L.i('--点击清空缓存按钮--')
            sleep(2)
            get_id(self, 'tv.yunxi.app:id/dialog_ok').click()
            sleep(2)
            L.i('--点击清空缓存dialog--')
            sleep(2)
            get_id(self, 'tv.yunxi.app:id/ll_back').click()
            sleep(2)
            self.driver.keyevent(4)  # 硬件返回
        except:
            L.w('--操作失败--')

        sleep(2)


if __name__ == '__My__':
    unittest.main()
