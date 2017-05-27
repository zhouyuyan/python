#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by zhouyuyan on 2017/5/26 12:04
import os
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from utils import L

from exception.exceptions import NotFoundTextError, NotFoundElementError

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


def find_element(self, loc):
    '''封装单个元素定位方法'''
    try:
        WebDriverWait(self.driver, 15.).until(lambda driver: driver.find_element(*loc).is_displayed())
        return self.driver.find_element(*loc)

    except Exception as e:
        print(u"%s 页面中未能找到 %s 元素" % (self, loc))
    return False

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


def _find_text_in_page(self, text):
    """检查页面中是否有文本关键字
    拿到页面全部source,暴力检查text是否在source中
    Args:
        text: 检查的文本

    Returns:
        True : 存在

    """
    print("[查找] 文本 %s " % text)
    return text in self.driver.page_source


def is_text_displayed(self, text, is_retry=True, retry_time=5, is_raise=False):
    """检查页面中是否有文本关键字

    如果希望检查失败的话,不再继续执行case,使用 is_raise = True

    Args:
        text: 关键字(请确保想要的检查的关键字唯一)
        is_retry: 是否重试,默认为true
        retry_time: 重试次数,默认为5
        is_raise: 是否抛异常
    Returns:
        True: 存在关键字
    Raises:
        如果is_raise = true,可能会抛NotFoundElementError

    """

    try:
        if is_retry:
            return WebDriverWait(self.driver, retry_time).until(
                lambda driver: _find_text_in_page(self, text))
        else:
            return _find_text_in_page(self, text)
    except TimeoutException:
        print("[Text]页面中未找到 %s 文本" % text)
        if is_raise:
            raise NotFoundTextError
        else:
            return False


def swip_down(self, count=1, method=None):
    """向下滑动,常用于下拉刷新

    Args:
        count: 滑动次数
        method: 传入的方法 method(action) ,如果返回为True,则终止刷新

    Examples:
        swip_down(self, count=100, method=is_text_displayed(self, "没有更多了"))
        上面代码意思:当页面不展示"暂无可配送的订单"时停止刷新,即有单停止刷新
    """
    window_size = self.driver.get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    if count == 1:
        self.driver.swipe(width / 2, height * 2 / 5, width / 2, height * 4 / 5, 2000)
        time.sleep(1)
    else:
        for x in range(count):
            self.driver.swipe(width / 2, height * 2 / 5, width / 2, height * 4 / 5, 2000)
            time.sleep(1)
            try:
                if method(self):
                    break
            except:
                pass


def swip_up(self, count=1, method=None):
    """向上滑动,常用于上拉加载

    Args:
        count: 滑动次数
        method: 传入的方法 method(action) ,如果返回为True,则终止加载

    Examples:
        swip_down(self, count=100, method=is_text_displayed(self, "没有更多了"))
        上面代码意思:当页面不展示"暂无可配送的订单"时停止加载,即有单停止加载
    """
    window_size = self.driver.get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    if count == 1:
        self.driver.swipe(width / 2, height * 4 / 5, width / 2, height * 2 / 5, 2000)
        time.sleep(1)
    else:
        x = 0
        for x in range(count):
            self.driver.swipe(width / 2, height * 4 / 5, width / 2, height * 2 / 5, 2000)
            time.sleep(1)
            try:
                if method(self):
                    break
            except:
                pass
        L.i('上拉加载的次数：' + str(x))


def _find_element(self, locator, is_need_displayed=True):
    """查找单个元素,如果有多个返回第一个

    Args:
        locator: 定位器
        is_need_displayed: 是否需要定位的元素必须展示

    Returns: 元素

    Raises: NotFoundElementError
            未找到元素会抛 NotFoundElementError 异常

    """
    if 'timeOutInSeconds' in locator:
        wait = locator['timeOutInSeconds']
    else:
        wait = 20

    try:
        if is_need_displayed:
            WebDriverWait(self.driver, wait).until(
                lambda driver: self._get_element_by_type(driver, locator).is_displayed())
        else:
            WebDriverWait(self.driver, wait).until(
                lambda driver: self._get_element_by_type(driver, locator) is not None)
        return self._get_element_by_type(self.driver, locator)
    except Exception as e:
        print("[element] 页面中未能找到 %s 元素" % locator)
        raise NotFoundElementError


def _find_elements(self, locator):
    """查找多元素(不会抛异常)

    Args:
        locator: 定位器

    Returns:元素列表 或 []

    """
    if 'timeOutInSeconds' in locator:
        wait = locator['timeOutInSeconds']
    else:
        wait = 20

    try:
        WebDriverWait(self.driver, wait).until(
            lambda driver: self._get_element_by_type(driver, locator, False).__len__() > 0)
        return self._get_element_by_type(self.driver, locator, False)
    except:
        print("[elements] 页面中未能找到 %s 元素" % locator)
        return []


@staticmethod
def _get_element_by_type(driver, locator, element=True):
    """通过locator定位元素(默认定位单个元素)

    Args:
        driver:driver
        locator:定位器
        element:
            true:查找单个元素
            false:查找多个元素

    Returns:单个元素 或 元素list

    """
    value = locator['value']
    ltype = locator['type']
    print("[查找]元素 %s " % locator)
    if ltype == 'name':
        ui_value = 'new UiSelector().textContains' + '(\"' + value + '\")'
        return driver.find_element_by_android_uiautomator(
            ui_value) if element else driver.find_elements_by_android_uiautomator(ui_value)
    else:
        return driver.find_element(ltype, value) if element else driver.find_elements(ltype, value)


def _send_key_event(self, arg, num=0):
    """
    操作实体按键
    Code码：https://developer.android.com/reference/android/view/KeyEvent.html
    Args:
        arg: event_list key
        num: KEYCODE_NUM 时用到对应数字

    """
    event_list = {'KEYCODE_HOME': 3, 'KEYCODE_BACK': 4, 'KEYCODE_MENU': 82, 'KEYCODE_NUM': 8}
    if arg == 'KEYCODE_NUM':
        self.driver.press_keycode(8 + int(num))
    elif arg in event_list:
        self.driver.press_keycode(int(event_list[arg]))
