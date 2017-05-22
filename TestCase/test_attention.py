#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/19 14:35
import unittest
from time import sleep
from Common import yunxiCommon as yc
from appium import webdriver as appdriver
from TestCase.test_login import Login as lg


class Attention(unittest.TestCase):
    def setUp(self):

        self.driver = appdriver.Remote('http://localhost:4723/wd/hub', yc.desired_caps(self))

        self.driver.implicitly_wait(5)

        print("----------------setup-------------")

    def tearDown(self):
        print("-------------teardown------------------")
        self.driver.close_app()
        self.driver.quit()

    def test_d(self):
        """测试登录-关注页面"""
        lg.login(self, '13071825896', '3279')
        self.attention()

    def attention(self):
        at = self.driver.find_element_by_name('关注')
        self.assertIsNotNone(at)
        at.click()
        tabs = self.driver.find_elements_by_id('tv.yunxi.app:id/tv_tab_title')
        self.assertIsNotNone(tabs)
        tabs[0].click()
        try:
            self.driver.find_element_by_id('tv.yunxi.app:id/tv_to_obsever')
            print(u'您关注的主播不在直播中')
            self.driver.find_element_by_id('tv.yunxi.app:id/tv_to_obsever').click()
            self.driver.find_element_by_id('tv.yunxi.app:id/img_activity_bg').click()
            sleep(2)
        except:
            print(u'关注列表不为空，请随便点击一个播放')
            self.driver.keyevent(4)
