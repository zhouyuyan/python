#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/26 12:04
import os
import time

"""""屏幕滑动方法"""


def get_id(self, id):
    element = self.driver.find_element_by_id(id)
    return element


def get_name(self, name):
    element = self.driver.find_element_by_name(name)
    return element


def get_xpath(self, xpath):
    element = self.driver.find_element_by_xpath(xpath)
    return element


def over(self):
    element = self.driver.quit()
    return element


def get_screen(self, path):
    self.driver.get_screenshot_as_file(path)


def swipe_to_up(self):
    window_size = self.driver.get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4, 500)


def swipe_to_down(self):
    window_size = self.driver.get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    self.driver.swipe(width / 2, height / 4, width / 2, height * 3 / 4, 500)


def swipe_to_left(self):
    window_size = self.driver.get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    self.driver.swipe(width / 4, height / 2, width * 3 / 4, height / 2, 500)


def swipe_to_right(self):
    window_size = self.driver.get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    self.driver.swipe(width * 4 / 5, height / 2, width / 5, height / 2, 500)


def swip_left(self, count=1):
    """向左滑动,一般用于ViewPager

    Args:
        count: 滑动次数

    """
    window_size = self.driver.get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    for x in range(count):
        time.sleep(1)
        self.driver.swipe(width * 9 / 10, height / 2, width / 10, height / 2, 1500)


def swip_right(self, count=1):
    """向右滑动,一般用于ViewPager

    Args:
        count: 滑动次数

    """
    window_size = self.driver.get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    for x in range(count):
        time.sleep(1)
        self.driver.swipe(width * 9 / 10, height / 10, width / 2, height / 2, 1500)


def back(self):
    self.driver.keyevent(4)


def get_classes(self, classesname):
    elements = self.driver.find_elements_by_class_name(classesname)
    return elements


def get_ids(self, ids):
    elements = self.driver.find_elements_by_id(ids)
    return elements


"""""封装查找元素及自动等待方法"""""


def find_elements(self, loc):
    '''封装一组元素定位方法'''
    try:
        if len(self.driver.find_elements(*loc)):
            return self.driver.find_elements(*loc)
    except Exception as e:
        print(u"%s 页面中未能找到 %s 元素" % (self, loc))
        return False


# def find_element(self, loc):
#     '''封装单个元素定位方法'''
#     try:
#         WebDriverWait(self.driver, 15.).until(lambdadriver: driver.find_element(*loc).is_displayed())
#         return self.driver.find_element(*loc)
#
# except Exception as e:
# print(u"%s 页面中未能找到 %s 元素" % (self, loc))
# return False

"""""保存图片"""


def take_Shot(self, name):
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    fp = "..\\Result\\" + day
    tm = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    type = '.png'

    filename = ''
    if os.path.exists(fp):
        filename = fp + "\\" + tm + '_' + name + type
    else:
        os.makedirs(fp)
        filename = fp + "\\" + tm + '_' + name + type
    self.driver.save_screenshot(filename)
