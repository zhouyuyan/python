#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/19 14:34
import unittest
from random import choice
from time import sleep
from Common.yunxiCommon import *
from TestCase.test_login import Login as lg
from appium import webdriver as appdriver


class Home(unittest.TestCase):
    def setUp(self):

        self.driver = appdriver.Remote('http://localhost:4723/wd/hub', desired_caps(self))

        self.driver.implicitly_wait(5)

        print("----------------setup-------------")

    def tearDown(self):
        print("-------------teardown------------------")
        self.driver.close_app()
        self.driver.quit()

    def test_a(self):
        """测试登录-发现-搜索-评论"""

        lg.login(self, '13071825896', '3279')
        self.goto_faxian()
        self.search()
        self.pinglun()

    def test_b(self):
        """测试登录-发现页面-关注-评论"""

        lg.login(self, '13071825896', '3279')
        self.faxian()
        self.guanzhu()

    def test_c(self):
        """测试未登录-发现页面-搜索"""

        self.goto_faxian()
        self.search()

    def test_sharefriend(self):
        """测试登录-发现页面-分享到微信/朋友圈"""

        lg.login(self, '13071825896', '3279')
        self.goto_faxian()
        self.search()
        self.wx_share()
        # self.wx_cricle()

    def test_videoSetting(self):
        """测试登录-发现页面-播放界面设置"""

        self.goto_faxian()
        self.search()
        # self.faxian()
        self.video_setting()

    def test_f(self):
        """测试登录-发现-评论"""
        lg.login(self, '13071825896', '3279')
        self.faxian()
        self.pinglun()

    # def test_g(self):
    #     """测试发现-播放页面设置"""
    #     self.faxian()
    #     self.video_setting()
    #     print("---------------------this is test_g-----------------------")

    def search(self):
        ser = self.driver.find_element_by_id('tv.yunxi.app:id/img_right')
        self.assertIsNotNone(ser)
        ser.click()
        print(u'--点击搜索按钮--')
        sleep(2)
        self.driver.find_element_by_id('tv.yunxi.app:id/ed_search').send_keys(u'啊啊啊啊啊')
        print(u'--输入搜索内容--')
        self.driver.keyevent(66)
        sleep(5)
        try:
            self.driver.find_element_by_id('tv.yunxi.app:id/tv_search_title')
            print(u'搜索成功')
            self.driver.find_element_by_id('tv.yunxi.app:id/img_search').click()


        except:
            print(u'搜索失败')
            pass
            self.driver.keyevent(4)

    def faxian(self):
        # 发现页面
        self.driver.find_element_by_name('发现').click()
        print(u'--进入发现页面--')
        sleep(2)

        self.driver.find_element_by_id('tv.yunxi.app:id/img_activity_bg').click()  # 点击视频直播
        print(u'--点击视频直播--')
        sleep(6)

    def goto_faxian(self):
        fx = self.driver.find_element_by_name('发现')
        fx.click()
        print(u'--进入发现页面--')
        sleep(2)

    def pinglun(self):
        # 详情页评论
        mylist = [u'很好', u'不错', u'赞', u'好看', u'受用']
        message = choice(mylist)
        self.driver.find_element_by_id('tv.yunxi.app:id/tv_input_click').click()
        # sleep(2)
        # 多条评论-----
        i = 1
        while (i < 200):
            self.driver.find_element_by_id('tv.yunxi.app:id/tv_input_click').send_keys(message + str(i))
            self.driver.keyevent(66)  # 发送
            i = i + 1
        newmessage = u'13071825896' + ':' + ' ' + ' ' + message + str(i)
        print(newmessage)
        message1 = self.driver.find_elements_by_id('tv.yunxi.app:id/tv_content')
        for ms in message1:
            if ms.text == newmessage:
                print(u'消息发送成功')
                break
                # ------一条评论------
                # self.driver.find_element_by_id('tv.yunxi.app:id/tv_input_click').send_keys(message)
                # self.driver.keyevent(66)  # 发送
                # newmessage = u'13071825896' + ':' + ' ' + ' ' + message
                # print(newmessage)
                # message1 = self.driver.find_elements_by_id('tv.yunxi.app:id/tv_content')
                # for i in message1:
                #     if i.text == newmessage:
                #         print(u'消息发送成功')
                #         break
                # sleep(2)

    def guanzhu(self):
        try:
            self.driver.find_element_by_id('tv.yunxi.app:id/img_up_head').click()
            sleep(2)
            print(u'--点击主播头像，进入企业主页--')

            self.driver.find_element_by_id('tv.yunxi.app:id/tv_to_observe').click()
            print(u'--点击关注--')

            sleep(4)
            self.driver.find_element_by_id('tv.yunxi.app:id/tv_to_observe').click()
            print(u'--再次点击关注--')
            sleep(2)

            self.driver.keyevent(4)
            self.driver.find_element_by_id('tv.yunxi.app:id/img_activity_bg').click()
            sleep(2)
            print(u'--点击企业列表--')

            self.driver.find_element_by_id('tv.yunxi.app:id/tv_to_observe').click()
            print(u'--直播页面点击关注--')
            sleep(2)
            self.driver.find_element_by_id('tv.yunxi.app:id/tv_to_observe').click()
            print(u'--直播页面再次点击关注--')
            sleep(2)
            self.driver.keyevent(4)
            sleep(3)

        except:
            print(u'--发现--')

    def video_setting(self):
        try:
            self.fusc = get_id(self, 'tv.yunxi.app:id/img_full_Screen')
            giftLl = get_id(self, 'tv.yunxi.app:id/giftLl')
            self.result01 = self.assertIsNotNone(self.fusc)
            print(self.result01)
            if (self.result01 == None):
                giftLl.click()
                self.fusc.click()
                print(u"点击屏幕")

            else:
                print(u"pass")
                self.fusc.click()
            print("横屏播放成功")
        except:
            print("横屏播放")
        sleep(5)
        bottom_control = get_id(self, 'tv.yunxi.app:id/rl_bottom_control')
        danm = get_id(self, 'tv.yunxi.app:id/img_danmaku_control')
        result02 = self.assertIsNotNone(danm)
        try:
            if (result02 == None):
                bottom_control.click()
                danm.click()
                print(u"点击屏幕")

            else:
                print(u"准备开启弹幕")
                danm.click()
            print("弹幕开启成功")

        except:
            print('failed_opentanmu')
        sleep(5)

        try:
            if (result02 == None):
                bottom_control.click()
                danm.click()

                print(u"点击屏幕")
            else:
                print(u"准备关闭tanmu")
                danm.click()
            print("弹幕关闭成功")
        except Exception as e:
            print('failed_closetanmu')
        sleep(5)

        # 关闭全屏
        try:
            if (self.result01 == None):
                bottom_control.click()
                self.fusc.click()
                print(u"关闭全屏")
            else:
                self.fusc.click()
                print(u"关闭全屏")
            print("全屏关闭成功")
        except:
            print("全屏关闭失败")

        self.driver.keyevent(4)  # 测试

    def wx_share(self):
        # 微信分享
        try:
            if self.assertIsNotNone(self.share):
                self.play.click()
                self.share.click()
            else:
                self.share.click()

            sleep(2)
            self.driver.find_element_by_xpath("//android.widget.LinearLayout[@index='0']").click()
            sleep(10)
            self.driver.find_element_by_xpath("//android.widget.LinearLayout[@index='1']").click()
            sleep(2)
            self.driver.find_element_by_name(u'分享').click()
            sleep(2)
            self.driver.find_element_by_name(u'返回云犀直播').click()
            sleep(3)
        except:
            print(u"分享到好友失败")

    def wx_cricle(self):
        # 朋友圈分享
        try:
            self.play = self.driver.find_element_by_id('tv.yunxi.app:id/ll_player_control')
            self.share = self.driver.find_element_by_id('tv.yunxi.app:id/img_activity_share')  # 进入到详情界面
            if self.assertIsNotNone(self.share):
                print(self.assertIsNotNone(self.share))
                self.play.click()
                self.share.click()
            else:
                self.share.click()
            sleep(2)
            self.driver.find_element_by_xpath("//android.widget.LinearLayout[@index='1']").click()
            sleep(2)
            self.driver.find_element_by_xpath("//android.widget.TextView[@text='发送']").click()
        except:
            print(u"分享到胖友圈失败")
