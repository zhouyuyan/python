# -*-coding:utf-8-*-
import os
import sys
import time
from imp import reload

from appium import webdriver

from Common import BasePage

reload(sys)
sys.setdefaultencoding('utf-8')
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from threading import Thread


class ActionKey(BasePage.AppAction):
    '''封装关键字方法'''

    def __init__(self, nowFunc):
        self.nowFunc = nowFunc

    def openApp(self, toast, plN, plV, dN, app, aPa, aAc, udid, uKey=True, reKey=True):
        '''打开app'''
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',
                                       self.set_desCaps(self.nowFunc, toast, plN, plV, dN, app, aPa, aAc, udid, uKey,
                                                        reKey))
        self.driver.implicitly_wait(30)

    def login(self, username, password, userinput, pwdinput, submit):
        '''
        登录
        :param username: 用户名
        :param password: 密码
        :param userinput: 用户名输入框
        :param pwdinput: 密码输入框
        :param submit: 提交登录
        :return: 
        '''
        self.send_key(userinput, username)
        self.send_key(pwdinput, password)
        self.click(submit)

    # 重写click
    def click(self, loc):
        '''
        点击
        :param loc: 元素定位方式
        :return: 无
        '''
        # print 'contexts_00:', self.driver.contexts
        # print 'page_source_00:',self.driver.page_source
        status_page = True
        while status_page:
            if (
                                        u'正在刷新..' or u'正在执行..' or u'正在加载..' or u'Loading..' or u'请稍等..' or u'请稍后..') not in self.driver.page_source:
                status_page = False
        i = 1
        while i < 3:
            try:
                ele = WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(loc))
                time.sleep(.5)
                ele.click()
                break
            except:
                try:
                    location, size = self.getElementSize(loc)
                    x = location.get('x')
                    y = location.get('y')
                    width = size.get('width')
                    height = size.get('height')
                    end_x = int(x) + int(width)
                    end_y = int(y) + int(height)
                    self.tap(end_x / 2, end_y / 2)
                    break
                except Exception as e:
                    print(u'元素第{}次点击失败！'.format(i))
            i += 1
            time.sleep(1)
        if i == 3:
            self.savePngName('元素点击失败', 'error')
            raise e

    # 切换到webview
    def switch_web(self):
        '''切换到webview页面'''
        try:
            self.switch_to_webview()
        except Exception as e:
            print(u'webview页面切换失败{}'.format(str(e)))
            self.savePngName('页面切换失败')

    # 切换到app
    def switch_app(self):
        '''切换到app页面'''
        try:
            self.switch_to_app()
        except Exception as e:
            print(u'app页面切换失败{}'.format(str(e)))
            self.savePngName('app页面切换失败')

    # 输入文字
    def input_text(self, loc, values):
        '''在文本框中输入文字
        :param loc:元素定位方式
        :param values:输入的内容
        '''
        try:
            self.send_key(loc, values)
        except Exception as e:
            print(u'输入异常{}'.format(str(e)))
            self.savePngName('输入异常')

    def mulClick(self, loc, indexs):
        '''
        多次点击
        :param loc: 元素定位方式
        :param indexs: 点击的index
        :return: 
        '''
        index = indexs.strip().strip('[').strip(']')
        indexs = index.split(',')
        for index in indexs:
            if str(index).isdigit():
                try:
                    self.find_elements_i(int(index) - 1, loc).click()
                except Exception as e:
                    print(u'多选失败：{}'.format(str(e)))
                    self.savePngName('元素多选失败', 'error')

    def Prints(self, loc):
        '''
        打印文本
        :param loc: 元素定位
        :return: 无
        '''
        text = self.find_element(loc).get_attribute('text')
        print(u'获取元素{}的显示信息：{}'.format(loc, text))

    def swipe_page(self, direction, n=1, duration=1000):
        '''滑动页面
        :param direction:滑动方向
        :param duration:持续时长
        '''
        # time.sleep(2)
        # print 'contexts_01:',self.driver.contexts
        # print 'page_source_01:', self.driver.page_source

        status_page = True
        while status_page:
            if (
                                        u'正在刷新..' or u'正在执行..' or u'正在加载..' or u'Loading..' or u'请稍等..' or u'请稍后..') not in self.driver.page_source:
                status_page = False
        try:
            for i in range(n):
                self.swipePage(direction, duration)
        except Exception as e:
            print(u'页面滑动失败{}'.format(str(e)))
            self.savePngName('页面滑动失败', 'error')
            raise e
        time.sleep(.5)

    def swipe_element(self, direction, loc, n=1, duration=1000):
        '''滑动元素
        :param direction:滑动方向
        :param loc:元素定位方式
        :param dyration:持续时长
        :param n:滑动次数
        '''
        try:
            for i in range(n):
                self.swipeElement(direction, loc, duration)
        except Exception as e:
            print(u'元素滑动失败:{}'.format(str(e)))
            self.savePngName('页面滑动失败', 'error')
            raise e

    def element_click(self, loc):
        '''点击操作
        :param loc:元素定位方式
        '''
        print(u'点击元素%s' % loc)
        self.find_element(loc).click()

    def assertData(self, loc, text):
        '''
        断言
        :param loc: 元素定位方式
        :param text: 预期值
        :return: True、False
        '''
        try:
            actual = self.find_element(loc).text
            print(u'预期结果：%s' % text)
            print(u'实际结果：%s' % actual)
        except Exception as e:
            print(u'验证查找元素失败{}'.format(str(e)))
            self.savePngName('验证查找元素失败')
        if actual != text:
            # self.saveScreenShot('预期结果与实际结果不符')
            self.savePngName('预期结果与实际结果不符')
            print(u'匹配不符！')
        else:
            print(u'匹配成功！')

    # def sqlDB(self, host, user, pwd, db, sql):
    #     '''
    #     执行sql
    #     :param host: 数据库地址
    #     :param user: 数据库用户名
    #     :param pwd: 数据库密码
    #     :param db: 数据库名
    #     :param sql: 执行的sql
    #     :return: 执行结果
    #     '''
    #     ms = connectsql.Mysql(host, user, pwd, db)
    #     return ms.executeSql(sql)
    #
    # def DBassert(self, actual, expect):
    #     '''
    #     数据库运行结果对比
    #     :param actual: 实际值
    #     :param expect: 预期值
    #     :return: 无
    #     '''
    #     print
    #     u'预期值：%s' % expect
    #     print
    #     u'实际值：%s' % actual
    #     assert actual == expect

    def tap_act(self, position, duration=550):
        '''
        模拟多手指点击
        :param position: 所以点击的坐标，比如：(123,234),(345,769),(443,129)
        :param duration: 持续时长
        :return: 无
        '''
        time.sleep(1)
        try:
            self.tap(position, duration)
        except Exception as e:
            print(u'屏幕点击失败{}'.format(str(e)))
            self.savePngName('屏幕点击失败')

    def drag_drop(self, loc1, loc2):
        '''
        元素拖拽
        :param loc1: 拖动的元素定位方式
        :param loc2: 目标元素定位方式
        :return: 无
        '''
        time.sleep(.5)
        try:
            self.dragAndDrop(loc1, loc2)
            time.sleep(.5)
        except Exception as e:
            print(u'元素拖动失败{}'.format(str(e)))
            self.savePngName('元素拖拽失败')

    def pinch_zoom_page(self, how, n=1):
        '''
        放大缩小页面
        :param how: 放大还是缩小
        :param n: 次数
        :return: 无
        '''
        # self.saveScreenShot('页面%s_前'%how)
        try:
            for i in range(n):
                self.p_z_page(how)
        except Exception as e:
            print(u'页面放大缩小失败{}'.format(str(e)))
            self.savePngName('页面放大缩小失败')
            # self.saveScreenShot('页面%s_后'%how)

    def pinch_zoom_ele(self, loc, how, n=1):
        '''
        放大缩小元素
        :param loc: 元素定位方式
        :param how: 放大还是缩小
        :param n: 次数
        :return: 无
        '''
        try:

            for i in range(n):
                self.p_z_element(loc, how)
        except Exception as e:
            print(u'元素放大缩小失败{}'.format(str(e)))
            self.savePngName('元素放大缩小失败')

    def shake_window(self):
        '''摇晃手机'''
        self.shake()

    def submit(self, loc):
        self.saveScreenShot('提交表单')
        self.click(loc)

    def set_net(self, connectType):
        '''
        设置网络类型
        :param connectType: 网络类型
        :return: 无
        '''
        try:
            self.setNetWork(connectType)
        except Exception as e:
            print(u'网络设置失败{}'.format(str(e)))
            self.savePngName('网络设置失败')
            # self.saveScreenShot('设置网络%s'%connectType)

    def toggle(self):
        '''定位'''
        try:
            self.toggleLocation()
        except Exception as e:
            print(u'GPS设置失败{}'.format(str(e)))
            self.savePngName('GPS设置失败')

    def save_img(self, name):
        '''
        手动截图
        :param name: 截图命名
        :return: 无
        '''
        try:
            self.savePngName(name, 'img')
        except Exception as e:
            print(u'手动截图失败{}'.format(str(e)))

    def install(self):
        '''安装app'''
        try:
            self.install_app()
        except Exception as e:
            print(u'安装失败{}'.format(str(e)))
            self.savePngName('安装失败')

    def uninstall(self):
        '''卸载app'''
        try:
            self.uninstall_app()
        except Exception as e:
            print(u'卸载失败{}'.format(str(e)))
            self.savePngName('卸载失败')

    def close(self):
        self.driver.close_app()
        time.sleep(1)

    def log(self):
        '''
        记录日志
        :return:无 
        '''

        dir2 = 'log\\Client'
        dir3 = 'log\\Run'
        if not os.path.exists(dir2):
            os.makedirs(dir2)

        if not os.path.exists(dir3):
            os.makedirs(dir3)
        now = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        logName = now + '_app'
        file = dir2 + '\\' + logName + '.log'
        filepath = os.path.abspath(file)
        command = 'adb logcat -v time -s *:E > ' + filepath
        print(u'执行命令：', command)
        os.system(command)

    def appiumServer(self):
        '''
        启动appium 服务
        :return: 无
        '''
        dir1 = 'log\\AppiumServer'
        if not os.path.exists(dir1):
            os.makedirs(dir1)
        now = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        name = now + '_appium'
        file = dir1 + '\\' + name + '.log'
        filepath = os.path.abspath(file)
        command = 'appium -a 127.0.0.1 -p 4723 --log-timestamp --log-level debug --local-timezone --session-override>' + filepath
        print(u'执行命令：', command)
        t2 = threading.Thread(target=os.system, args=(command,))
        t2.setDaemon(True)
        t2.start()

    def stop_Appium(self):
        cmd = 'StopAppium.bat 4723'  # print cmd
        p = os.popen(cmd)
        print(u'关闭appium')
        print
        (p.read())

    def setTime(self, loc, loc2, time2):
        '''
        设置日期
        :param y: 年
        :param m: 月
        :param d: 日
        :param H: 时
        :param M: 分
        :param S: 秒
        :return: 
        '''
        loc1 = self.find_element(loc)
        loc1.click()

        po, ele = self.getElementSize(loc2)
        width = ele['width']
        height = ele['height']
        x = po['x']
        y = po['y']

        y_x = x + width * 31 / 216  # 169
        m_x = x + width * 123 / 360  # 365
        d_x = x + width * 173 / 360  # 518
        H_x = x + width * 223 / 360  # 667
        M_x = x + width * 273 / 360  # 819
        S_x = x + width * 323 / 360  # 965

        start_y = y + height * 13 / 50
        end_y = y + height / 2

        time2 = str(time2).strip()
        print('目标时间', time2)
        self.click(['xpath', u'//*[contains(@text,"确定")]'])
        time.sleep(1)
        loc1 = self.find_element(loc)
        time1 = loc1.text
        print('当前时间', time1)
        time1 = str(time1).strip()
        y, m, d, H, M, S = self.rootTime(time1)
        y1, m1, d1, H1, M1, S1 = self.rootTime(time2)
        loc1.click()
        time.sleep(1)

        num_y = abs(y1 - y)
        num_m = abs(m1 - m)
        num_d = abs(d1 - d)
        num_H = abs(H1 - H)
        num_M = abs(M1 - M)
        num_S = abs(S1 - S)

        if y < y1:
            self.thread('up', y_x, start_y, y_x, end_y, num_y)
        elif y > y1:
            self.thread('down', y_x, start_y, y_x, end_y, num_y)
        if m < m1:
            self.thread('up', m_x, start_y, m_x, end_y, num_m)
        elif m > m1:
            self.thread('down', m_x, start_y, m_x, end_y, num_m)
        if d < d1:
            self.thread('up', d_x, start_y, d_x, end_y, num_d)
        elif d > d1:
            self.thread('down', d_x, start_y, d_x, end_y, num_d)
        if H < H1:
            self.thread('up', H_x, start_y, H_x, end_y, num_H)
        elif H > H1:
            self.thread('down', H_x, start_y, H_x, end_y, num_H)
        if M < M1:
            self.thread('up', M_x, start_y, M_x, end_y, num_M)
        elif M > M1:
            self.thread('down', M_x, start_y, M_x, end_y, num_M)
        if S < S1:
            self.thread('up', S_x, start_y, S_x, end_y, num_S)
        elif S > S1:
            self.thread('down', S_x, start_y, S_x, end_y, num_S)

        self.click(['xpath', u'//*[contains(@text,"确定")]'])

    def setTime2(self, loc, loc2, time2):
        '''
        设置日期
        :param y: 年
        :param m: 月
        :param d: 日
        :param H: 时
        :param M: 分
        :param S: 秒
        :return: 
        '''
        loc1 = self.find_element(loc)
        loc1.click()

        po, ele = self.getElementSize(loc2)
        width = ele['width']
        height = ele['height']
        x = po['x']
        y = po['y']

        y_x = x + width / 8  # 150
        m_x = x + width * 3 / 8  # 370
        d_x = x + width / 2  # 545
        H_x = x + width * 3 / 4  # 730
        M_x = x + width * 7 / 8  # 915
        # S_x = 965

        start_y = y + height * 13 / 50
        end_y = y + height / 2

        time2 = str(time2).strip()
        print('目标时间', time2)
        self.click(['xpath', u'//*[contains(@text,"确定")]'])
        time.sleep(1)
        loc1 = self.find_element(loc)
        time1 = loc1.text
        print('当前时间', time1)
        time1 = str(time1).strip()
        y, m, d, H, M, S = self.rootTime(time1)
        y1, m1, d1, H1, M1, S1 = self.rootTime(time2)
        loc1.click()
        time.sleep(1)

        num_y = abs(y1 - y)
        # print 'num_y',num_y
        num_m = abs(m1 - m)
        # print 'num_m',num_m
        num_d = abs(d1 - d)
        # print 'num_d',num_d
        num_H = abs(H1 - H)
        # print 'num_H',num_H
        num_M = abs(M1 - M)
        # print 'num_M',num_M
        num_S = abs(S1 - S)

        if y < y1:
            self.thread('up', y_x, start_y, y_x, end_y, num_y)
        elif y > y1:
            self.thread('down', y_x, start_y, y_x, end_y, num_y)
        if m < m1:
            self.thread('up', m_x, start_y, m_x, end_y, num_m)
        elif m > m1:
            self.thread('down', m_x, start_y, m_x, end_y, num_m)
        if d < d1:
            self.thread('up', d_x, start_y, d_x, end_y, num_d)
        elif d > d1:
            self.thread('down', d_x, start_y, d_x, end_y, num_d)
        if H < H1:
            self.thread('up', H_x, start_y, H_x, end_y, num_H)
        elif H > H1:
            self.thread('down', H_x, start_y, H_x, end_y, num_H)
        if M < M1:
            self.thread('up', M_x, start_y, M_x, end_y, num_M)
        elif M > M1:
            self.thread('down', M_x, start_y, M_x, end_y, num_M)

        self.click(['xpath', u'//*[contains(@text,"确定")]'])

    def thread(self, direction, x, start_y, x2, end_y, n):
        '''
        设置日期线程
        :param direction: 方向
        :param x: 起始坐标x
        :param start_y: 起始坐标y
        :param x2: 终止坐标x
        :param end_y: 终止坐标y
        :param n: 滑动次数
        :return: 无
        '''
        if direction.upper() == 'UP':
            t1 = Thread(target=self.flicks, args=(x, end_y, x2, start_y, n))
        elif direction.upper() == 'DOWN':
            t1 = Thread(target=self.flicks, args=(x, start_y, x2, end_y, n))
        t1.start()
        t1.join()

    def Back(self):
        '''
        回退操作
        :return: 无
        '''
        time.sleep(.5)
        self.driver.back()

    def Forward(self):
        '''
        前进操作，还未实现
        :return: 无
        '''
        time.sleep(.5)
        self.driver.forward()
